# lightHPC
A light HPC pack base on AWS managed services as Lambda &amp; DynamoDB

基于 Lambda + DynamoDB 托管服务构建灵巧型 HPC 集群

适用场景Scenarios:

（1）	弱耦合型：计算过程中间很少数据交互；

（2）	随来随算：HPC的算力构建基于事件触发，能即时响应；

（3）	数据切分：计算任务可基于数据维度来分解并行的；

（4）	运维零压：部署完成后，平时基本是零维护和零管理；

（5）	足够节省：平时运维低费用，且算完及时回收资源以降成本。


脚本文件构成:

fLightScheduler.py -- Lambda function of dispatching compute transactions and launching compute instances.   
jobrun.py -- Compute node simulation script.
fRlstProc.py -- Lambda function of result processing and SNS notification.
fMissionCfg.py -- Lambda function of mission parameters configuration.


数据流程说明：
本场景里的计算是将样本文件与海量已知样本数据做匹配分析计算，我们将一个计算任务（Mission）按照不同的样本比对区间切分成多个分片计算事务（Transactions）。

（1）	分析任务的输入是由样本文件上传至S3源端bucket来触发，处理Lambda函数（lightScheduler）负责划分计算事务并将Mission和Transactions的信息记入DynamoDB的任务信息表（tblMission）和事务信息表（tblTrans）中，并发起启动对应数量的Spot实例。

（2）	Spot实例根据计算节点的AMI镜像启动，根据源文件名和事务表记录信息执行计算脚本，计算完成后结果文件输出至S3存储的result桶，并自行Terminate终止实例。

（3）	结果文件以消息驱动结果处理函数（RsltProc）来进行结果汇集和计算任务完成通知。

（4）	计算任务的配置通过Lambda配置函数（MissionCfg）来写入tblMission表。


