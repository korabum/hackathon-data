#* @post /log
log_regression<-function(timestamp){

  default_result_file_name <- "prediksi_score_all"
  default_function_initial <- "lr"
  local_path <- "/home/collin/R_Script/hack_a_ton"

  csv_result_file_name <- paste(default_result_file_name,"_",as.character(timestamp),".csv",sep="")
  json_file_name <- paste(default_function_initial,"_",as.character(timestamp),".json",sep="")
  csv_file_name <- paste(default_function_initial,"_",as.character(timestamp),".csv",sep="")

  setwd(local_path)

  #Read json data
  library(rjson)
  input_target<-fromJSON(file = json_file_name)
  
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
  model <- glm(paste(input_target$target, "~."),family=binomial(link='logit'),data=train)
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
  
  return (csv_result_full_path)
}