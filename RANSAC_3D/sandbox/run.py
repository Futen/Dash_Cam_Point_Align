import numpy as np
import dataset
import networkx as nx
import json

if __name__ == '__main__':
    
    f_name = 'tracks.csv'
    f = open(f_name, 'r')
    obj, graph_feature_data, graph_track_data = dataset.load_tracks_graph(f)  #####
    #print graph_track_data
    f.close()
    track_nodes, image_nodes = nx.algorithms.bipartite.sets(obj) ####

    f = open('reconstruction.json', 'r')
    buf = json.load(f)[0]
    image_lst = buf['shots'].keys() #####
    reconstruct_data = buf['points'] ####
    reconstruct_data_key_lst = reconstruct_data.keys() #####
    f.close()
    match_data = np.load('data_hog_00002_and40.npy').item()
    #print match_data.keys()
    #print 'image-00092' in match_data.keys()
    f = open('data.json', 'r')
    pano_data = json.load(f)
    f.close()
    #print pano_data.keys()
    new_pano_data = {}
    for index, key in enumerate(pano_data):
        #print key
        loc_key = pano_data[key].keys()[0]
        pano_key = match_data[key].keys()[0]
        tmp = np.reshape(pano_data[key][loc_key], (-1,3))
        try:
            new_pano_data[key + '.jpg'][pano_key] = tmp
        except:
            new_pano_data[key + '.jpg'] = {}
            new_pano_data[key + '.jpg'][pano_key] = tmp

    #print new_pano_data.keys()
    recontruct_point = []
    pano_point = []
    for index, key in enumerate(match_data):
        #print key
        key_tmp = key + '.jpg'
        if key_tmp in image_lst:
            #print 'iiii'
            pano_key = match_data[key].keys()[0]
            for index, image_index in enumerate(match_data[key][pano_key][0]):
                #print type(image_index)
                if image_index in graph_feature_data[key_tmp]:
                    #print 'ggg'
                    track_id = graph_track_data[key_tmp][str(image_index)]
                    if track_id in reconstruct_data_key_lst:
                        point1 = reconstruct_data[track_id]['coordinates']
                        point2 = new_pano_data[key_tmp][pano_key][index, :]
                        if point2[np.abs(point2) > 10000].size == 0:
                            recontruct_point.append(point1)
                            pano_point.append(point2)
    recontruct_point = np.array(recontruct_point, dtype=np.float32)
    #length = recontruct_point.shape[0]
    #recontruct_point = np.array([recontruct_point[:,0], recontruct_point[:,1], recontruct_point[:,2], np.ones([length])], dtype=np.float32)
    pano_point = np.array(pano_point, dtype = np.float32)
    #pano_point = np.array([pano_point[:,0], pano_point[:,1], pano_point[:,2], np.ones([length])], dtype=np.float32)
    np.save('result.npy', [recontruct_point, pano_point])
    print recontruct_point.shape
    print pano_point.shape








