from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

if __name__ == "__main__":
    es = Elasticsearch(['esheader01.ihep.ac.cn'], http_auth=('elastic', 'mine09443'), timeout=3600)
    #配置需要的字段
    offsetfields={"includes":["host","@timestamp","host","fsname","jobid","off1","off2"],"excludes":[]}
    offsetquery_json={
        "bool": {
            "must": [
                {
                    "query_string": {
                        "query": "*"
                    }
                },
                {
                    "range": {
                        "@timestamp": {
                            # "gte": 1560445679880,
                            # "lte": 1569721086880,
                            "gte": 1569686400000,
                            "lte": 1569721086880,
                            "format": "epoch_millis"
                        }
                    }
                }
            ]
        }
    }
    queryData = es.search(index='search_lustreclientactionoffset', scroll='5m', timeout='3s', size=100, body={"_source":offsetfields,"query":offsetquery_json})
    mdata = queryData.get("hits").get("hits")
    if not mdata:
        print('empty!')

    scroll_id = queryData["_scroll_id"]
    total = queryData["hits"]["total"]
    for i in range(int(total/100)):
        res = es.scroll(scroll_id=scroll_id, scroll='5m') #scroll参数必须指定否则会报错
        mdata += res["hits"]["hits"]
        print(res)
    #打印获取的es数据
    print(mdata)

    ###################################################################
    #配置需要的字段
    extentfields={"includes":["host","@timestamp","host","fsname","jobid","ext1","ext2","ext3","ext4","ext5","ext6","ext7","ext8","ext9","ext10","ext11","ext12","ext13","ext14","ext15","ext16","ext17","ext18","ext19","ext20","ext21","ext22","ext23","ext24"],"excludes":[]}
    extentquery_json={
        "bool": {
            "must": [
                {
                    "query_string": {
                        "query": "*"
                    }
                },
                {
                    "range": {
                        "@timestamp": {
                            "gte": 1560445679880,
                            "lte": 1569721086880,
                            "format": "epoch_millis"
                        }
                    }
                }
            ]
        }
    }
    queryData = es.search(index='search_lustreclientactionextent', scroll='5m', timeout='3s', size=100, body={"_source":extentfields,"query":extentquery_json})
    mdata = queryData.get("hits").get("hits")
    if not mdata:
        print('empty!')

    scroll_id = queryData["_scroll_id"]
    total = queryData["hits"]["total"]
    for i in range(int(total/100)):
        res = es.scroll(scroll_id=scroll_id, scroll='5m') #scroll参数必须指定否则会报错
        mdata += res["hits"]["hits"]
        print(res)
    #打印获取的es数据
    print(mdata)

##########################################################
    #配置需要的字段
    mdsfields={"includes":["host","@timestamp","host","fsname","jobid","rename","setattr","getattr","statfs","mkdir","getxattr","sync","setxattr","mknod","link","rmdir","samedir_rename","close","unlink","open","crossdir_rename"],"excludes":[]}
    mdsquery_json={
        "bool": {
            "must": [
                {
                    "query_string": {
                        "query": "*"
                    }
                },
                {
                    "range": {
                        "@timestamp": {
                            "gte": 1560445679880,
                            "lte": 1569721086880,
                            # "gte": 1560445679880,
                            # "lte": 1560446400000,
                            "format": "epoch_millis"
                        }
                    }
                }
            ]
        }
    }
    queryData = es.search(index='search_lustreclientactionmds', scroll='5m', timeout='3s', size=100, body={"_source":mdsfields,"query":mdsquery_json})
    mdata = queryData.get("hits").get("hits")
    if not mdata:
        print('empty!')

    scroll_id = queryData["_scroll_id"]
    total = queryData["hits"]["total"]
    for i in range(int(total/100)):
        res = es.scroll(scroll_id=scroll_id, scroll='5m') #scroll参数必须指定否则会报错
        mdata += res["hits"]["hits"]
        print(res)
    #打印获取的es数据
    exit()
    ############deal data###########
    #将第一条es数据写入新的index
    #es.index(index="mlganglia_agg", doc_type="doc", body=mdata[0]['_source'])
    #批量写入
    ACTION=[]
    for unit in mdata:
        #根据nodename和time创建key
        id=unit['_source']['nodename'].replace(".ihep.ac.cn","")+"_"+str(unit['_source']['time'])
        action = {
            "_index":"mlganglia_agg",
            "_type":"doc",
            "_id":id,
            "_source":unit['_source'],
            "_op_type":"index"
        }
        ACTION.append(action)
        if len(ACTION)>=500:
            success, _ = bulk(es, ACTION,index="mlganglia_agg")
            print("Performed %d actions" % success)
            #清空ACTION
            ACTION=[]
    if len(ACTION):
        success, _ = bulk(es, ACTION,index="mlganglia_agg")
        print("Performed %d actions" % success)

    #条件删除
    #es.delete_by_query(index='mlganglia_agg', body={"query":query_json})
    #批量更新
    ACTION=[]
    for unit in mdata:
        #根据nodename和time计算出key
        id=unit['_source']['nodename'].replace(".ihep.ac.cn","")+"_"+str(unit['_source']['time'])
        action = {
            "_index":"mlganglia_agg",
            "_type":"doc",
            "_id":id,
            "doc":{"new1value":0.49,"tags":["tag1","tag3"]},
            "_op_type":"update"
        }
        ACTION.append(action)
        if len(ACTION)>=500:
            success, _ = bulk(es, ACTION,index="mlganglia_agg")
            print("Performed %d actions" % success)
            #清空ACTION
            ACTION=[]
    if len(ACTION):
        success, _ = bulk(es, ACTION,index="mlganglia_agg")
        print("Performed %d actions" % success)
