package main

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

var status = true
var deviceStatus = false
var commandData = ""
var replyData = ""

func postCommandData(writer http.ResponseWriter, request *http.Request) {
	params := mux.Vars(request)
	command := params["command_data"]
	if command != "" {
		status = true
		commandData = command
		fmt.Println(command)
	} else {
		status = false
	}
}

func postReplyData(writer http.ResponseWriter, request *http.Request) {
	params := mux.Vars(request)
	reply := params["reply_data"]
	if reply != "" {
		deviceStatus = true
		replyData = reply
	} else {
		deviceStatus = false
	}
}

func checkStatus(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if status { c = 1}
	_ = json.NewEncoder(writer).Encode(c)
}

func checkDeviceStatus(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if deviceStatus { c = 1}
	_ = json.NewEncoder(writer).Encode(c)
}

func setStatus(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(status)
}

func setDeviceStatus(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(deviceStatus)
}

func getCommadData(writer http.ResponseWriter, request *http.Request) {
	status = false
	_ = json.NewEncoder(writer).Encode(commandData)
	fmt.Println(status)
}

func getReplyData(writer http.ResponseWriter, request *http.Request) {
	deviceStatus = false
	_ = json.NewEncoder(writer).Encode(replyData)
	fmt.Println(deviceStatus)
}

func main() {
	router := mux.NewRouter()
	router.HandleFunc("/post_data/{command_data}", postCommandData).Methods("POST")
	router.HandleFunc("/post_reply_data/{reply_data}", postReplyData).Methods("POST")
	router.HandleFunc("/check_status/", checkStatus).Methods("GET")
	router.HandleFunc("/check_device_status/", checkDeviceStatus).Methods("GET")
	router.HandleFunc("/set_status/", setStatus).Methods("POST")
	router.HandleFunc("/set_device_status/", setDeviceStatus).Methods("POST")
	router.HandleFunc("/get_command_data/", getCommadData).Methods("GET")
	router.HandleFunc("/get_reply_data/", getReplyData).Methods("GET")
	_ = http.ListenAndServe(":5000", router)
}
