# change the local_path to your workspace where the csv, json request and csv result will be
local_path <- "."
setwd(local_path)

#* @post /fort/log
log_regression<-function(file_name, target){
  default_result_file_name <- "prediksi_score_all"
  default_function_initial <- "output/lr"

  print(file_name)
  print(target)

  now <- format(Sys.time(), "%Y%m%d%H%M%S")

  csv_result_file_name <- paste(default_function_initial,"_",as.character(now),".csv",sep="")
  csv_file_name <- file_name

  #Read json data
  library(rjson)
  input_target <- target
  
  #Read csv data
  training.data.raw <- read.csv(csv_file_name,header=T,na.strings=c(""))
  training.data<-training.data.raw
  
  #Change data type for discrete variable
  training.data$E_X_aic_ipctry_issue<-as.factor(training.data$E_X_aic_ipctry_issue)
  training.data$E_X_trx_last<-as.factor(training.data$E_X_trx_last)
  training.data$learning_label<-as.factor(training.data$learning_label)
  
  #Take specific colums from dataframe
  data <- subset(training.data,select=c(2,3,4,5,6,7,8,9,10,11,14))
  
  #Split dataframe to training and testing
  train <- data[1:floor((nrow(data)*0.8)),]
  test <- data[floor((nrow(data)*0.8)+1):nrow(data),]
  
  #Build model
  model <- glm(paste(input_target, "~."),family=binomial(link='logit'),data=train)
  # model <- glm(paste(target),family=binomial(link='logit'),data=train)
  summary(model)
  
  #Predict data using model
  fitted.results2 <- predict(model,newdata=subset(data,select=c(1,2,3,4,5,6,7,8,9,10)),type='response')
  
  #Make score ranging from 0-1000
  a22<-floor(fitted.results2*1000)
  
  #Creating output id, ..., R_score
  a2<-as.data.frame(a22)
  a3<-cbind(training.data.raw$id, training.data.raw$blacklist, training.data.raw$whitelist, training.data.raw$learning_label, a2$a22)
  colnames(a3) <- c("ID","Blacklist","Whitelist","Learning_Label", "R_Score")
  a4<-as.data.frame(a3)

  

  write.csv(a4,file = csv_result_file_name, row.names = FALSE)
  csv_result_full_path <- paste(local_path,"/",csv_result_file_name,sep="")
  response <- list(status= 200,output= paste(normalizePath(csv_result_full_path)))
  
  return (toJSON(response))
}

#* @post /fort/rforest
rforest <- function(file_name,target){

  default_result_file_name <- "res_all_h2o"
  default_function_initial <- "output/rf"

  now <- format(Sys.time(), "%Y%m%d%H%M%S")

  csv_result_file_name <- paste(default_result_file_name,"_",as.character(now),".csv",sep="")
  # json_file_name <- paste(default_function_initial,"_",as.character(timestamp),".json",sep="")
  csv_file_name <- file_name
  
  setwd(local_path)

  library(h2o)
  localH2O = h2o.init(ip = 'localhost', port = 54321)
  
  library(rjson)
  # input_target<-fromJSON(file = json_file_name)
  input_target <- target
  
  # Import data
  data_raw <- read.csv(csv_file_name, header=T, na.string=c(""))
  
  data = data_raw
  
  train_raw <- data_raw[1:floor((nrow(data_raw)*0.8)),]
  test_raw <- data_raw[floor((nrow(data_raw)*0.8)+1):nrow(data_raw),]
  
  data$E_X_aic_ipctry_issue<-as.factor(data$E_X_aic_ipctry_issue)
  data$E_X_trx_last<-as.factor(data$E_X_trx_last)
  data$learning_label<-as.factor(data$learning_label)
  
  train <- data[1:floor((nrow(data)*0.8)),]
  test <- data[floor((nrow(data)*0.8)+1):nrow(data),]
  
  train.h2o = as.h2o(train)
  test.h2o = as.h2o(test)
  
  summary(train)
  summary(test)
  summary(train.h2o)
  summary(test.h2o)
  
  # independent variables
  y.dep = input_target
  x.indep = c(2:11)
  
  #Random Forest
  system.time(rforest.model <- h2o.randomForest(y = y.dep, x=x.indep, training_frame = train.h2o, ntrees = 20, mtries = 3, max_depth = 4, seed = 1122))
  
  h2o.performance(rforest.model)
  
  #check variable importance
  h2o.varimp(rforest.model)
  
  # produce prediction results from the developed model (no bruce_id here)
  pred_train_h2o = as.data.frame(predict(rforest.model, train.h2o))
  pred_test_h2o = as.data.frame(predict(rforest.model, test.h2o))
  
  # combining with bruce_id
  res_train = cbind(train_raw$id, train_raw$blacklist, train_raw$whitelist, train_raw$learning_label, pred_train_h2o$p1)
  res_test = cbind(test_raw$id, test_raw$blacklist, test_raw$whitelist, test_raw$learning_label, pred_test_h2o$p1)
  
  res_train = as.data.frame(res_train)
  res_test = as.data.frame(res_test)
  res_all = as.data.frame(rbind(res_train,res_test))
  
  colnames(res_train) = c("ID","Blacklist","Whitelist","Learning_Label","H2o_Score")
  colnames(res_test) = c("ID","Blacklist","Whitelist","Learning_Label","H2o_Score")
  colnames(res_all) = c("ID","Blacklist","Whitelist","Learning_Label","H2o_Score")
  
  res_all$H2o_Score = floor(res_all$H2o_Score*1000)
  
  # write.csv(res_train, "res_train.csv", row.names = FALSE)
  # write.csv(res_test, "res_test.csv", row.names = FALSE)
  write.csv(res_all, csv_result_file_name, row.names = FALSE)
  csv_result_full_path <- paste(local_path,"/",csv_result_file_name,sep="")

  return (csv_result_full_path)
}

