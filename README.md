# lightHPC
A light HPC pack base on AWS managed services as Lambda &amp; DynamoDB

Scenarios:

Loose coupled HPC which parallelized by data zone;

Driven by input file event;

Nearly zero management during usual operations.


List:

fNewFileNote.py -- Lambda function of dispatching compute transactions and launching compute instances.   

jobrun.py -- Compute node simulation script.

fRlstProc.py -- Lambda function of result processing and SNS notification.

fMissionCfg.py -- Lambda function of mission parameters configuration.


