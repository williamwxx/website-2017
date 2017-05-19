#!/usr/bin/env bash


set -e



usage(){
    echo "Usage: $0 -g|--group <项目组> \n\
                    -n|--name <项目名> \n\
                    -e|-env <项目环境> \n\
                    -l|--label <项目标签> \n\
                    -r|--redis <redis> \n\
                    -t|--type <项目类型ui、java> \n\
                    -h|--help <帮助> "

}


while [[ $# -gt 1 ]]
do
key="$1"
case $key in
    -g|--group)
    KS_PROJECT_GROUP=$2
    shift;;
    -n|--name)
    KS_PROJECT_NAME=$2
    shift;;
    -e|--env)
    KS_PROJECT_STATUS=$2
    shift;;
    -l|--label)
    GO_PIPELINE_LABEL=$2
    shift;;
    -r|--redis)
    KS_REDIS_SERVER=$2
    shift;;
    -t|--type)
    GO_ENVIRONMENT_NAME=$2
    shift;;
    -h|--help)
    usage
    shift;;
esac
shift
done


if [ -z $KS_PROJECT_GROUP ] || [ -z $KS_PROJECT_NAME ] || [ -z $KS_PROJECT_STATUS ] || [ -z $GO_PIPELINE_LABEL ] || [ -z $KS_REDIS_SERVER ];then
    usage
    exit 1
fi

echo "==============================="
echo "== KS_PROJECT_GROUP : $KS_PROJECT_GROUP"
echo "== KS_PROJECT_NAME : $KS_PROJECT_NAME"
echo "== KS_PROJECT_STATUS : $KS_PROJECT_STATUS"
echo "== GO_PIPELINE_LABEL : $GO_PIPELINE_LABEL"
echo "==============================="





copyJava(){

    echo "创建目录[app] ....."
    mkdir -p app/libs && mkdir -p app/bin && mkdir app/resources
    echo "拷贝[jar]到app/libs/ ....."
    cp target/*.jar app/libs/
    if [[ $KS_PROJECT_NAME == "zdcrm-reporting" ]]; then
        cp -r src/main/resources/* app/resources/
    fi
    echo "拷贝[reload_conf.sh]到 app/bin/ ......"
    #cp /data/ContinuousDeployment/deploy/serviceManager.py app/bin/
    cp /data/ContinuousDeployment/deploy/reload_conf.sh app/bin/

    #app/bin/reload_conf.sh zdcrm-ws.properties
    #app/bin/reload_conf.sh unionpay.properties
    echo "初始化配置文件,从配置中心拉取 ....."
#    chmod a+x app/bin/reload_conf.sh
#    app/bin/reload_conf.sh all
}

copyUi(){
    echo "创建目录[app]"
    mkdir -p app

    if [ -f "index.html" ];then
        echo "拷贝index.html"
        cp index.html app/
    fi
    if [ -d "dist" ];then
        echo "拷贝dist目录"
        cp -r dist app/
    else
        echo "dist 目录不存在 .."
        exit 1
    fi

}

if [ ! -d "app" ];then
    if [[ $GO_ENVIRONMENT_NAME == "JAVA" ]] || [[ $GO_ENVIRONMENT_NAME == "java" ]];then
        copyJava
    elif [[ $GO_ENVIRONMENT_NAME == "ui" ]] || [[ $GO_ENVIRONMENT_NAME == "UI" ]] || [[ $GO_ENVIRONMENT_NAME == "NODEJS" ]] || [[ $GO_ENVIRONMENT_NAME == "nodejs" ]];then
        copyUi
    else
        echo "GO_ENVIRONMENT_NAME MUST BE IN [java,ui,nodejs]"
        exit 1
    fi

else
    echo "目录app 已经存在"
fi



echo "拷贝app到远程目录[/data/$KS_PROJECT_GROUP/$KS_PROJECT_NAME.$GO_PIPELINE_LABEL] ..."
ansible $KS_PROJECT_GROUP -m copy -a "src=app/ dest=/data/$KS_PROJECT_GROUP/$KS_PROJECT_NAME.$GO_PIPELINE_LABEL"

echo "拷贝serviceManager.py到远程目录 ..."
ansible $KS_PROJECT_GROUP -m copy -a "src=/data/ContinuousDeployment/deploy/serviceManager.py dest=/data/$KS_PROJECT_GROUP"

echo "从配置文件夹拷贝配置文件"
ansible $KS_PROJECT_GROUP -m script -a "/data/ContinuousDeployment/deploy/copy_resources.sh -g $KS_PROJECT_GROUP -n $KS_PROJECT_NAME -l $GO_PIPELINE_LABEL"


#echo "赋予.sh可执行权限 ...."
#ansible $KS_PROJECT_GROUP -m shell -a "chmod a+x /data/${KS_PROJECT_GROUP}/${KS_PROJECT_NAME}.${GO_PIPELINE_LABEL}/bin/*.sh"

echo "执行serviceManager.py ....."
ansible ${KS_PROJECT_GROUP} -m script -a "/data/ContinuousDeployment/deploy/serviceManager.py --action start --redis $KS_REDIS_SERVER --project $KS_PROJECT_NAME --env $KS_PROJECT_STATUS --group $KS_PROJECT_GROUP --label $GO_PIPELINE_LABEL --user chenyongbing --password kashuo"
