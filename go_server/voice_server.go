package main

import (
	"strconv"
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

var command_status = false
var reply_status = false
var path_updated = true
var path_updated_mobile = true

var code_update = false
var code_update_mobile = false

var default_state = 0

var command_data = ""
var reply_data = ""

var current_path_data path_var

var code code_meta_data 

type dir struct {
	Type string `json:"type"`
	Name string `json:"name"`
}

type path_var struct {
	Path string `json:"path"`
	PathData []dir `json:"path_data"`
}

type code_meta_data struct {
	Code string `json:"code"`
}

func postCommandData(writer http.ResponseWriter, request *http.Request) {
	params := mux.Vars(request)
	command := params["command_data"]
	if command != "" {
		command_status = true
		command_data = command
		fmt.Println(command)
	} else {
		command_status = false
	}
}

func postReplyData(writer http.ResponseWriter, request *http.Request) {
	params := mux.Vars(request)
	reply := params["reply_data"]
	reply_status = true
	reply_data = reply
	fmt.Println("Reply POSTED")
}

func checkStatus(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if command_status { c = 1}
	_ = json.NewEncoder(writer).Encode(c)
}

func checkDeviceStatus(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if reply_status { c = 1}
	_ = json.NewEncoder(writer).Encode(c)
}

func setStatus(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(command_status)
}

func setDeviceStatus(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(reply_status)
}

func getCommandData(writer http.ResponseWriter, request *http.Request) {
	command_status = false
	_ = json.NewEncoder(writer).Encode(command_data)
	fmt.Println(command_status)
}

func postPathData(writer http.ResponseWriter, request *http.Request) {
	decoder := json.NewDecoder(request.Body)
	var json_data path_var
	_ = decoder.Decode(&json_data)
	fmt.Println(json_data)
	current_path_data = json_data
	path_updated = true
	path_updated_mobile = true
}

func getPathUpdateStatus(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if path_updated { c = 1 }
	_ = json.NewEncoder(writer).Encode(c)
}

func getPathUpdateStatusMobile(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if path_updated_mobile { c = 1 }
	_ = json.NewEncoder(writer).Encode(c)
}

func getPathData(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(current_path_data)
	path_updated = false
	fmt.Println("POSTED")
}

func getPathDataMobile(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(current_path_data)
	path_updated_mobile = false
	fmt.Println(path_updated_mobile)
}

func setDefaultState(writer http.ResponseWriter, request *http.Request) {
	parms := mux.Vars(request)
	state := parms["df_state"]
	default_state,_ = strconv.Atoi(state)
	fmt.Println(default_state)
}

func getDefaultState(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(default_state)
}

func getReplyData(writer http.ResponseWriter, request *http.Request) {
	reply_status = false
	_ = json.NewEncoder(writer).Encode(reply_data)
	fmt.Println(reply_data)
}

func getCodeData(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(code)
	fmt.Println(code)
	code_update = false
}

func getCodeDataMobile(writer http.ResponseWriter, request *http.Request) {
	_ = json.NewEncoder(writer).Encode(code)
	fmt.Println("MOBILE GOT CODE")
	code_update_mobile = false
}

func postCodeData(writer http.ResponseWriter, request *http.Request) {
	decoder := json.NewDecoder(request.Body)
	var c_code code_meta_data
	_ = decoder.Decode(&c_code)
	code = c_code
	code_update = true
	code_update_mobile = true
	fmt.Println("POSTED")
}

func getCodeStatus(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if code_update { c = 1 }
	_ = json.NewEncoder(writer).Encode(c)
}

func getCodeStatusMobile(writer http.ResponseWriter, request *http.Request) {
	c := 0
	if code_update_mobile { c = 1 }
	_ = json.NewEncoder(writer).Encode(c)
}

func main() {
	fmt.Println("ENTERING MAIN")
	router := mux.NewRouter()
	router.HandleFunc("/post_data/{command_data}", postCommandData).Methods("POST")
	router.HandleFunc("/post_reply_data/{reply_data}", postReplyData).Methods("POST")
	router.HandleFunc("/check_status/", checkStatus).Methods("GET")
	router.HandleFunc("/check_device_status/", checkDeviceStatus).Methods("GET")
	router.HandleFunc("/set_status/", setStatus).Methods("POST")
	router.HandleFunc("/set_device_status/", setDeviceStatus).Methods("POST")
	router.HandleFunc("/get_command_data/", getCommandData).Methods("GET")
	router.HandleFunc("/get_reply_data/", getReplyData).Methods("GET")
	router.HandleFunc("/path_data/", postPathData).Methods("POST")
	router.HandleFunc("/get_path_data/", getPathData).Methods("GET")
	router.HandleFunc("/get_path_data_mobile/", getPathDataMobile).Methods("GET")
	router.HandleFunc("/get_path_update_status/", getPathUpdateStatus).Methods("GET")
	router.HandleFunc("/get_path_update_status_mobile/", getPathUpdateStatusMobile).Methods("GET")
	router.HandleFunc("/set_default_state/{df_state}", setDefaultState).Methods("POST")
	router.HandleFunc("/get_default_state/", getDefaultState).Methods("GET")
	router.HandleFunc("/post_code/", postCodeData).Methods("POST")
	router.HandleFunc("/get_code/", getCodeData).Methods("GET")
	router.HandleFunc("/get_code_mobile/", getCodeDataMobile).Methods("GET")
	router.HandleFunc("/get_code_status/", getCodeStatus).Methods("GET")
	router.HandleFunc("/get_code_status_mobile/", getCodeStatusMobile).Methods("GET")
	_ = http.ListenAndServe(":5000", router)
}

