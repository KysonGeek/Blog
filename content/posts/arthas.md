+++
title = "Arthas 使用记录"
date = 2025-12-09
weight = 20251209
description = "Arthas 是Alibaba开源的Java诊断工具，深受开发者喜爱。"

[taxonomies]
tags = ["研发", "工具"]

[extra]
+++
[Arthas 官网](https://arthas.aliyun.com/)
## 1、进入 webShell 下载 arthas
```bash
curl -O https://arthas.aliyun.com/arthas-boot.jar
```
## 2. 启动 arthas
方法一
```bash
webShell# java -jar arthas-boot.jar
[INFO] arthas-boot version: 3.5.5
[INFO] Found existing java process, please choose one and input the serial number of the process, eg : 1. Then hit ENTER.
* [1]: 364 web-app-1.21.4.jar
1 //输入上面的 jar前面的序号
```
方法二
```bash
#找到java进程的pid
webShell# ps -ef|grep java
webShell# java -jar arthas-boot.jar 364 # pid
```
## 3. 常用命令

```bash
watch com.xx.sdk.entity.EntityMetaUtils getEntitySchema "{params[0],throwExp}" -e -x 2

watch com.xx.application.service.FieldPageQueryService fillQuoteEntityFieldInfo "{params[1]}" -x 2

watch com.xx.runtime.container.factory.MarketContainerFactory loadDevComponentContainer "{returnObj.devSubscribeMap}" -x 2

watch com.xx.domain.versions.DevVersionQueryService getFromCache "{params, returnObj}" -x 2  '#cost>30'

watch com.xx.meta.execute.sdk.pipeline.PipelineService queryActivePipelineName "{params, returnObj}" -x 5

watch com.xxtask.dataimport.FieldService fieldTransform "{params,returnObj}" 'params[3].fieldName == "address__city"' -x 5

trace com.xx.util.mybatis.MetaDataAbstractReader loadOverrideData

watch com.xx.domain.bizsys.data.entity.DomainEntityMeta getFieldMetaList 'returnObj' -x 3 'returnObj[0].entityName == "Mar"'
watch com.xx.thrift.service.converter.EntityDetailConverter buildTemplateInfo "{params, returnObj}" -x 5 'params[1].name=="ppe_tongji01__c"'

watch com.xx.infrastructure.converter.entity.EntityFieldConverter convertInner 'params' 'params[1].entityName == "MarketingCampaignMember"'

trace com.xx.util.mybatis.MetaDataOverrideUtil loadOverrideData 'params[1][1].name == "validator_len__object_account__primaryName"'

classloader -t

ognl -c 6ad5c04e '#obj=new com.xx.common.i18n.I18nString("xxx.meta.button.show_name.create","xx"),@com.xx.common.i18n.I18nTranslateService@translate(@com.xx.common.enums.LanguageEnum@en, #obj)' -X 1
ognl -c 6ad5c04e '#obj=new com.xx.util.QueryContext("kyson_CN","","xxx",11111111,"",null,null), @com.xx.runtime.container.DataContainerFactory@loadTenantEntity(#obj)' -x 1

#obj=new com.xx.util.QueryContext("kyson_CN","","xxx",11111111,"",null,null)
ognl -c 6ad5c04e '#obj=@com.xx.util.QueryContext@newBuilder()@withTenantCode("kyson_CN")@build()'

ognl -c 6ad5c04e '#obj=@com.xx.util.QueryContext@newInst("xxx")'

ognl -c 6ad5c04e '#obj=@com.xx.util.QueryContext@newBuilder().withTenantCode("kyson_CN").withSys("xxx").withEmployeeId(11111111L)'

ognl -c 6ad5c04e '#obj=@com.xx.util.QueryContext@newBuilder().withTenantCode("kyson_CN").withSys("xxx").withEmployeeId(11111111L).build(), @com.xx.runtime.container.impl.DataContainerFactory@refreshPageRoute(#obj).suiteNamePageMap.get("1616140138847_eskqfthy")'

ognl -c 1be6f5c3 '#obj=com.xx.infrastructure.mapper.BizSelfMapper'
ognl -c 1be6f5c3 '#obj=@com.xx.util.SpringUtils@getBean("bizSelfMapper").getCurrentTimestamp()' -X 1


```