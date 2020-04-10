#!/bin/bash 

time="`date +%Y-%m-%d-%H-%M-%S`"
echo ${time}

# 项目 scheme 名称
project_scheme="Test"
# 指定项目下 build 编译目录（存放在工程根目录 build 文件里）
build_dir="./build"
# 指定项目下 archive 编译目录
temp_archive_dir=${build_dir}/archive/temp.xcarchive
ipa_dir=${build_dir}/ipa

# 配置蒲公英KEY
api_key="1342d4dd949c1bc97e9bfdf42ac77b78"
# 配置蒲公英更新描述信息
pgyer_desc="Test新包"


# 清理项目 build目录
echo "cleaning..."
if [ -d ${build_dir} ]
then
rm -rf ${build_dir}
echo -e "\n** CLEAN ARCHIVE FILE SUCCEED **\n"
fi


# build
echo "archiving..."
xcodebuild archive -scheme ${project_scheme} -archivePath ${temp_archive_dir} -configuration Release


# 打包ipa
echo "exporting..."
xcodebuild -exportArchive -archivePath ${temp_archive_dir}  -exportPath  ${ipa_dir}/${time} -exportOptionsPlist exportIpaOption.plist


#上传蒲公英
echo "uploading..."
ipa=${build_dir}/ipa/${time}/${project_scheme}.ipa
curl -F 'file=@'${ipa} -F '_api_key='${api_key}  -F 'buildUpdateDescription='${pgyer_desc} https://www.pgyer.com/apiv2/app/upload
echo -e "\n** UPLOAD TO PGYER SUCCEED **\n"
