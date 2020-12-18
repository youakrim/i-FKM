from bottle import route, run, template, request, static_file
from fuzzy_k_means import fuzzy_k_means
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import seaborn as sns
import cv2

def numpy_to_b64(array):
    print("shape:", array.shape)
    im_pil = Image.fromarray(array, 'RGB')
    if im_pil.mode != 'RGBA':
        im_pil = im_pil.convert('RGBA')
    buff = BytesIO()
    im_pil.save(buff, format="png")
    im_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    return im_b64

@route('/')
def index():
    return template('index')

@route('/img/<filename>')
def server_static(filename):
    return static_file(filename, root='img/')

@route('/style/<filename>')
def server_static(filename):
    return static_file(filename, root='style/')

@route('/compute_k_means', method='POST')
def compute_k_means():
    image_path = 'img/small_land.jpg'
    img = np.array(Image.open(image_path))
    X = np.reshape(img, (img.shape[0]* img.shape[1], 3))
    e = float(request.forms.get('e'))
    nb_clusters = int(request.forms.get('nb_clusters'))
    algo = request.forms.get('algo')

    cluster_colors = sns.color_palette("Set2", nb_clusters)
    print(algo)
    if algo == 'fuzzy_k_means':
        m = float(request.forms.get('m'))
        alpha = float(request.forms.get('a'))

        is_alpha_checked = request.forms.get('alpha_cut')
        is_alpha_checked = is_alpha_checked == 'true'
        print(is_alpha_checked)

        seg =fuzzy_k_means(e, X, nb_clusters, m=m)
        seg = np.reshape(seg, (img.shape[0], img.shape[1], nb_clusters))

        alpha_cut = (seg > alpha).astype(np.uint8)
        mask = np.zeros((img.shape[0], img.shape[1], 3))
        alpha_mask = np.zeros((img.shape[0], img.shape[1], 3))

        for y in range(0, img.shape[0]):
            for x in range(0, img.shape[1]):
                color = np.zeros(3, dtype=np.uint8)
                alpha_color = np.zeros(3, dtype=np.uint8)
                for c in range(0, nb_clusters):
                    color = color + seg[y, x, c]*np.array(cluster_colors[c])*255
                    alpha_color = color + alpha_cut[y, x, c]*np.array(cluster_colors[c])*255

                mask[y, x] = (color).astype(np.uint8)
                alpha_mask[y, x] = alpha_color

        mask = mask.astype(np.uint8)
        alpha_mask = alpha_mask.astype(np.uint8)

        if is_alpha_checked:
            mask = alpha_mask
    else:
        # k means
        compactness, seg, centers = cv2.kmeans(np.float32(X),nb_clusters,None,(cv2.TERM_CRITERIA_EPS, 10, e), attempts=1, flags=cv2.KMEANS_RANDOM_CENTERS)

        seg = np.reshape(seg, (img.shape[0], img.shape[1]))

        mask = np.zeros((img.shape[0], img.shape[1], 3))

        for y in range(0, img.shape[0]):
            for x in range(0, img.shape[1]):
                c = seg[y,x]
                mask[y, x] = np.array(cluster_colors[c])*255
        mask = mask.astype(np.uint8)

    return 'data:image/png;base64,'+str(numpy_to_b64(mask))

run(host='localhost', port=8080)
