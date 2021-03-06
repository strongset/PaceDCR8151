# -*- coding: utf-8 -*-
# Test name = Software Upgrade
# Test description = Set environment, perform software upgrade and check STB state after sw upgrade

from datetime import datetime
from time import gmtime, strftime
import time
import os.path
import sys
import device
import TEST_CREATION_API
import shutil

try:    
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py")) == False) or (str(os.path.getmtime('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py')) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))))):
        shutil.copy2('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py', os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))
except:
    pass

import NOS_API    
  
try:
    # Get model
    model_type = NOS_API.get_model()

    # Check if folder with thresholds exists, if not create it
    if(os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds")) == False):
        os.makedirs(os.path.join(os.path.dirname(sys.executable), "Thresholds"))

    # Copy file with threshold if does not exists or if it is updated
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt")) == False) or (str(os.path.getmtime(NOS_API.THRESHOLDS_PATH + model_type + ".txt")) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))))):
        shutil.copy2(NOS_API.THRESHOLDS_PATH + model_type + ".txt", os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))
except Exception as error_message:
    pass

##Set correct grabber for this TestSlot
NOS_API.grabber_type()

##Set correct grabber for this TestSlot
TEST_CREATION_API.grabber_type()

def runTest():
    System_Failure = 0
    Repeat = 0
    
    ## Reset all global variables 
    NOS_API.reset_test_cases_results_info()
                
    while(System_Failure < 2):
        try:           
            Upgrade_First_Test = 0
            while (Repeat < 2):
                Break_Cicle = False
                if (Repeat == 1):
                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                        Upgrade_First_Test = 1
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    TEST_CREATION_API.write_log_to_file("#################################################################____________________ Second Test ____________________################################################################")
                
            
                Software_Upgrade_TestCase = False
        
                Input_Signal_TestCase = False
        
                Serial_Number_TestCase = False
            
                ## Number of alphanumeric characters in SN
                SN_LENGTH = 16  
                
                ## Number of alphanumeric characters in Cas_Id
                CASID_LENGTH = 12
                
                ## Number of alphanumeric characters in MAC
                MAC_LENGTH = 12
                
                ## Set test result default to FAIL
                test_result = "FAIL"
                test_end = 1
                SW_UPGRADE_TIMEOUT = 500
        
                ## Time needed to STB power on (in seconds)
                WAIT_TO_POWER_STB = 15
                
                ## Time out after stb power on 
                TIMEOUT_CAUSE_SW_UPGRADE = 25
                
                ## Max time to perform sw upgrade (in seconds)
                WAIT_FOR_SEARCHING_SW = 300
                
                ## Threshold for ber value
                BER_VALUE_THRESHOLD = "1.0E-6"
        
                ## Threshold for snr value
                SNR_VALUE_THRESHOLD_LOW = 20
                SNR_VALUE_THRESHOLD_HIGH = 80
                
                Act = 0
                
                counter_black = 0
                
                Tentativas_Act = 0
                
                HDMI_No_Repeat = 0
                
                Num_Tentativas_Atualizcao = 6
                
                NOS_API.Upgrade_State = 0
                
                ## Set test result default to FAIL
                sw_version_prod = NOS_API.Firmware_Version_DCR_8151
                iris_version_prod = NOS_API.IRIS_Version_DCR_8151        
                
                NOS_API.read_thresholds()
        
                SN_LABEL = False
                CASID_LABEL = False
                MAC_LABEL = False
                
                ## Reset all global variables 
                #NOS_API.reset_test_cases_results_info()
                
                error_codes = ""
                error_messages = ""
                
                tx_value = "-"
                rx_value = "-"
                downloadstream_snr_value = "-"
                ip_adress = "-"
                sc_number = "-"
                cas_id_number = "-"
                sw_version = "-"
                snr_value = "-"
                ber_value = "-"
                modulation = "-"
                frequencia = "-"
        
                try:
                    ## Perform scanning with barcode scanner   
                    all_scanned_barcodes = NOS_API.get_all_scanned_barcodes()     
                    NOS_API.test_cases_results_info.s_n_using_barcode = all_scanned_barcodes[1]
                    NOS_API.test_cases_results_info.cas_id_using_barcode = all_scanned_barcodes[2]
                    NOS_API.test_cases_results_info.mac_using_barcode = all_scanned_barcodes[3]
                    NOS_API.test_cases_results_info.nos_sap_number = all_scanned_barcodes[0]
                except Exception as error:   
                    TEST_CREATION_API.write_log_to_file(error)
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                    NOS_API.set_error_message("Leitura de Etiquetas")
                    error_codes = NOS_API.test_cases_results_info.scan_error_code
                    error_messages = NOS_API.test_cases_results_info.scan_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                            test_result,
                            "- - - - - - - - - - - - - - - - - - - -",
                            "- - - - - - - - - - - - - - - - - - - -",
                            error_codes,
                            error_messages)
            
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                    NOS_API.upload_file_report(report_file)      
                    NOS_API.test_cases_results_info.isTestOK = False
                    
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
            
                    return                   
                
                
                test_number = NOS_API.get_test_number(NOS_API.test_cases_results_info.s_n_using_barcode)
                device.updateUITestSlotInfo("Teste N\xb0: " + str(int(test_number)+1))
                
                if ((len(NOS_API.test_cases_results_info.s_n_using_barcode) == SN_LENGTH) and (NOS_API.test_cases_results_info.s_n_using_barcode.isalnum() or NOS_API.test_cases_results_info.s_n_using_barcode.isdigit()) and (NOS_API.test_cases_results_info.cas_id_using_barcode != NOS_API.test_cases_results_info.mac_using_barcode)):
                    SN_LABEL = True
                
                if ((len(NOS_API.test_cases_results_info.cas_id_using_barcode) == CASID_LENGTH) and (NOS_API.test_cases_results_info.cas_id_using_barcode.isalnum() or NOS_API.test_cases_results_info.cas_id_using_barcode.isdigit())):
                    CASID_LABEL = True
                    
                if ((len(NOS_API.test_cases_results_info.mac_using_barcode) == MAC_LENGTH) and (NOS_API.test_cases_results_info.mac_using_barcode.isalnum() or NOS_API.test_cases_results_info.mac_using_barcode.isdigit())):
                    MAC_LABEL = True
                
                if not(SN_LABEL and CASID_LABEL and MAC_LABEL):
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                    NOS_API.set_error_message("Leitura de Etiquetas")
                    error_codes = NOS_API.test_cases_results_info.scan_error_code
                    error_messages = NOS_API.test_cases_results_info.scan_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                            test_result,
                            "- - - - - - - - - - - - - - - - - - - -",
                            "- - - - - - - - - - - - - - - - - - - -",
                            error_codes,
                            error_messages)
            
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                    NOS_API.upload_file_report(report_file)      
                    NOS_API.test_cases_results_info.isTestOK = False
                    
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
            
                    return
        ##############################################################################################################################################################################################################################    
        ###########################################################################################Software Upgrade###################################################################################################################    
        ##############################################################################################################################################################################################################################
                if(System_Failure == 1 or Repeat == 1):
                    NOS_API.configure_power_switch_by_inspection()
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        
                        NOS_API.set_error_message("POWER SWITCH")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                        error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                        error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                            test_result,
                            "- - - - - - - - - - - - - - - - - - - -",
                            "- - - - - - - - - - - - - - - - - - - -",
                            error_codes,
                            error_messages)
                
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)       
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        return

                ## Power on STB with energenie
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
        
                        NOS_API.set_error_message("POWER SWITCH")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                        error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                        error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        return
                    
                    time.sleep(1)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    
                    NOS_API.set_error_message("POWER SWITCH")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                    error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    NOS_API.add_test_case_result_to_file_report(
                            test_result,
                            "- - - - - - - - - - - - - - - - - - - -",
                            "- - - - - - - - - - - - - - - - - - - -",
                            error_codes,
                            error_messages)
                
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = NOS_API.create_test_case_log_file(
                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                NOS_API.test_cases_results_info.nos_sap_number,
                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                NOS_API.test_cases_results_info.mac_using_barcode,
                                end_time)
                    NOS_API.upload_file_report(report_file)
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                    return     
                NOS_API.give_me_give_me_give_me_a_time_after_finish("Descarregar Test Plan / Iniciar Grabber / Power ON")      
                if(System_Failure == 0 and Repeat == 0):
                    if not(NOS_API.display_new_dialog("Conectores?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"): 
                        TEST_CREATION_API.write_log_to_file("Conectores NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.conector_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.conector_nok_error_message)
                        NOS_API.set_error_message("Danos Externos")
                        error_codes = NOS_API.test_cases_results_info.conector_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.conector_nok_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                            
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        return
                    if not(NOS_API.display_new_dialog("Chassis?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"): 
                        TEST_CREATION_API.write_log_to_file("Chassis NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.chassis_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.chassis_nok_error_message) 
                        NOS_API.set_error_message("Danos Externos")
                        error_codes = NOS_API.test_cases_results_info.chassis_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.chassis_nok_error_message
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        return
                    if not(NOS_API.display_custom_dialog("Inserir SmartCard! A STB est\xe1 ligada?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):   
                        TEST_CREATION_API.write_log_to_file("No Power")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_power_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_power_error_message) 
                        NOS_API.set_error_message("Não Liga") 
                        error_codes =  NOS_API.test_cases_results_info.no_power_error_code
                        error_messages = NOS_API.test_cases_results_info.no_power_error_message
                        NOS_API.deinitialize()
                        
                        NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                    
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                    end_time)
                        NOS_API.upload_file_report(report_file)
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        return
                    
                NOS_API.grabber_hour_reboot()
                
                ## Initialize grabber device
                NOS_API.initialize_grabber()       
        
                ## Start grabber device with video on default video source
                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                
                while (Act < 2):
                    if (Act == 1):
                        Software_Upgrade_TestCase = False
                        Input_Signal_TestCase = False
                        while(Tentativas_Act < Num_Tentativas_Atualizcao):
                            #if not(NOS_API.change_usb_port("USBHUB-06##")):
                            NOS_API.Send_Serial_Key("a", "feito")
                            time.sleep(1)           
                            ## Power off STB with energenie
                            NOS_API.configure_power_switch_by_inspection()
                            if not(NOS_API.power_off()): 
                                TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                
                                NOS_API.set_error_message("POWER SWITCH")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                                error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                        
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                                NOS_API.upload_file_report(report_file)
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)       
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                return
                            time.sleep(3)
                            ## Power on STB with energenie
                            if not(NOS_API.power_on()):
                                TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                
                                NOS_API.set_error_message("POWER SWITCH")
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                                error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                            
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                                NOS_API.upload_file_report(report_file)
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                    
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                return
                            
                            time.sleep(TIMEOUT_CAUSE_SW_UPGRADE)
                    
                            if not(NOS_API.display_custom_dialog("A STB est\xe1 a atualizar?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                Tentativas_Act = Tentativas_Act + 1
                                if (Tentativas_Act == 5):
                                    NOS_API.Send_Serial_Key("d", "feito")
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                    NOS_API.deinitialize()
                                    NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                                
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                                    NOS_API.upload_file_report(report_file)
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    return
                            else:
                                if(NOS_API.test_cases_results_info.DidUpgrade == 2):
                                    NOS_API.test_cases_results_info.DidUpgrade = 3
                                elif(NOS_API.test_cases_results_info.DidUpgrade == 4):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                NOS_API.Upgrade_State = 1
                                Tentativas_Act = 6
                        
                        WAIT_FOR_SEARCHING_SW = 700          
        
                    # Get start time
                    start_time = time.localtime()
                    delta_time = 0
                    signal_detected_on_hdmi = False
                    signal_detected_on_cvbs = False
                    counter_ended = False
                    while(counter_ended == False):
                        TEST_CREATION_API.write_log_to_file(delta_time)
                        if(delta_time > WAIT_FOR_SEARCHING_SW):
                            counter_ended = True
                            break
        
                        # Reset flags
                        signal_detected_on_hdmi = False
                        signal_detected_on_cvbs = False
        
                        # Get current time and check is testing finished
                        delta_time = (time.mktime(time.localtime()) - time.mktime(start_time)) 
        
                        time.sleep(2)
                    
                        if not(NOS_API.is_signal_present_on_video_source()):
                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                            time.sleep(10)
                        
                        if (NOS_API.is_signal_present_on_video_source()):
                            time.sleep(5)
                            if (NOS_API.is_signal_present_on_video_source()):
                                result = NOS_API.wait_for_multiple_pictures(
                                                ["check_cables_HDMI", "Check_Por_Favor_HDMI", "Black_HDMI", "Black_HDMI_1080_ref", "Check_Por_Favor_HDMI_Shifted_ref"],
                                                4,
                                                ["[FULL_SCREEN_720]", "[FULL_SCREEN_576]", "[FULL_SCREEN_720]", "[FULL_SCREEN]", "[FULL_SCREEN_576]"],
                                                [80, 70, 80, 80, 70])
                                if(result == -1):
                                    signal_detected_on_hdmi = True
                                    signal_detected_on_cvbs = True
                                    if not (NOS_API.grab_picture("HDMI_Image")):
                                        continue
                                    break
                                elif(result == 2):
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    time.sleep(4)
                                    TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                    time.sleep(10)
                                    TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                    time.sleep(2)
        
                        ## Start grabber device with video on CVBS2
                        NOS_API.grabber_stop_video_source()
                        NOS_API.reset_dut()
        
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                        
                        if not(NOS_API.is_signal_present_on_video_source()):
                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                            time.sleep(10)
                        if (NOS_API.is_signal_present_on_video_source()):
                            time.sleep(5)
                            if (NOS_API.is_signal_present_on_video_source()):
                                result = NOS_API.wait_for_multiple_pictures_fast_picture_transition(
                                                ["black_screen_cvbs", "check_cables_CVBS", "check_cables_CVBS_1", "Check_Por_Favor_CVBS", "Check_Por_Favor_CVBS_1", "Check_Por_Favor_CVBS_old"],
                                                4,
                                                ["[FULL_SCREEN_576]", "[FULL_SCREEN_576]", "[FULL_SCREEN_576]", "[FULL_SCREEN_576]", "[FULL_SCREEN_576]", "[FULL_SCREEN_576]"],
                                                [80, 40, 40, 40, 40, 40])
                                if(result == -1):
                                    signal_detected_on_cvbs = True
                                    if not (NOS_API.grab_picture("Scart_Image")):
                                        NOS_API.grabber_stop_video_source()
                                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                        continue                                
                                else:
                                    ## if black screen or check power cable screen
                                    NOS_API.grabber_stop_video_source()
                                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                    continue
                            else:
                                NOS_API.grabber_stop_video_source()
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)                       
                                continue
                        else:
                            NOS_API.grabber_stop_video_source()
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)                       
                            continue
        
                        ## Start grabber device with video on HDMI1
                        NOS_API.grabber_stop_video_source()
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)                                 
        
                        if not(NOS_API.is_signal_present_on_video_source()):
                            NOS_API.display_dialog("Confirme o cabo HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            time.sleep(1)
                            HDMI_No_Repeat = 1
                            #if not(NOS_API.is_signal_present_on_video_source()):
                            #    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                            #time.sleep(10)
                        if (NOS_API.is_signal_present_on_video_source()):
                            time.sleep(5)
                            if (NOS_API.is_signal_present_on_video_source()):
                                result = NOS_API.wait_for_multiple_pictures(
                                                ["check_cables_HDMI", "Check_Por_Favor_HDMI", "Black_HDMI", "Black_HDMI_1080_ref", "Check_Por_Favor_CVBS_old"],
                                                4,
                                                ["[FULL_SCREEN_720]", "[FULL_SCREEN_576]", "[FULL_SCREEN_720]", "[FULL_SCREEN]", "[FULL_SCREEN_576]"],
                                                [80, 70, 80, 80, 70])
                                if(result == -1):
                                    signal_detected_on_hdmi = True
                                    if not (NOS_API.grab_picture("HDMI_Image")):
                                        continue
                                elif((result == 2 or result == 3) and signal_detected_on_cvbs == True):
                                    counter_black = counter_black + 1  
                                    time.sleep(10)
                                    if (counter_black < 2):
                                        continue
                                elif(result == 0 or result == 1 or result == -2):
                                    continue
                        else:
                            ## Start grabber device with video on CVBS2
                            NOS_API.grabber_stop_video_source()
                            NOS_API.reset_dut()
        
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                            
                            if not(NOS_API.is_signal_present_on_video_source()):
                                NOS_API.grabber_stop_video_source()
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                continue 
                                
                        if((signal_detected_on_hdmi == False) and (signal_detected_on_cvbs == True)):
                            if (HDMI_No_Repeat == 1):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI (Não Retestar)")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                                return    
                            else:
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                            
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                return    
        
                        if((signal_detected_on_hdmi == True) and (signal_detected_on_cvbs == True)):
                            break
        
                    if(counter_ended == True):
                        if (Repeat == 0):
                            Repeat = Repeat + 1
                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                NOS_API.test_cases_results_info.DidUpgrade = 3
                            else:
                                NOS_API.test_cases_results_info.DidUpgrade = 2
                            TEST_CREATION_API.write_log_to_file("STB didn't Boot. Line 870.")
                            break
                        else:
                            TEST_CREATION_API.write_log_to_file("No boot")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                            NOS_API.set_error_message("Não arranca")
                            error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                            NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
            
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                        
                            return                
                                        
                    if((signal_detected_on_hdmi == True) and (signal_detected_on_cvbs == True)):
                        
                        ## If STB is standby it happens that after 5 seconds text "POR FAVOR" appears for 3 seconds and then disappears
                        time.sleep(5)
                                        
                        start_time_standby_mode = time.localtime()
                        delta_time_standby = 0
                        delta_check = 60
                        while (delta_time_standby < SW_UPGRADE_TIMEOUT):
                            delta_time_standby = (time.mktime(time.localtime()) - time.mktime(start_time_standby_mode))     
                            if (NOS_API.is_signal_present_on_video_source()):
        
                                compare_result = NOS_API.wait_for_multiple_pictures(
                                                                    ["sw_upgrade_loop_3_ref", "sw_update_loop_1_720p", "sw_update_loop_2_720p", "sw_update_loop_2_720p_SD", "sw_update_error_720p_upg_ref", "sw_update_error_720p_eng_ref", "sw_update_error_720p", "Old_Shiffted_Image_ref", "searching_for_sw_1080_old_ref", "Inst_Old_Offset_eng_ref", "Inst_Old_Offset_ref", "UMA_Logo_ref",  "Menu_UMA_1080_ref", "ErrorMessage_ref", "Menu_New_1080_ref", "sd_service_720p_ref1", "sd_service_720p_ref2", "sd_service_720p_ref3", "sd_service_720p_ref4", "sd_service_ref1", "sd_service_ref2", "sd_service_ref3", "hd_channel_ref", "hd_channel_ref1", "hd_channel_ref2", "no_signal_channel_mode_ref", "no_signal_channel_mode_2_ref", "no_signal_channel_mode_720_ref", "no_signal_channel_mode_2_720_ref", "menu_576_ref", "menu_720_ref", "menu_1080_ref", "No_Channel_1", "error_message_1080_ref", "TermsConditions_ref", "installation_boot_up_ref", "installation_boot_up_ref1", "language_installation_mode_ref", "installation_text_installation_mode_ref", "english_installation", "english_termos", "english_language_installation_ref", "installation_boot_up_ref_old", "installation_boot_up_ref_old_1", "Installation_Check_Signal", "Upgrade_OK_ref"],
                                                                    delta_check,
                                                                    ["[SW_UPDATE_LOOP_3]", "[SW_UPDATE_LOOP_720p]", "[SW_UPDATE_LOOP_720p]", "[SW_UPDATE_LOOP_720p]", "[SW_UPDATE_ERROR_UPG_720p]", "[SW_UPDATE_ERROR_720p]", "[SW_UPDATE_ERROR_720p]", "[Old_Shiffted_Installation]", "[searching_for_sw_1080_ref]", "[Inst_Old_Offset]", "[Inst_Old_Offset]", "[UMA_Logo]", "[Def_UMA_Menu]", "[Menu_Error_Message]", "[Def_Symbol_1080]", "[HALF_SCREEN]", "[HALF_SCREEN]", "[HALF_SCREEN]", "[HALF_SCREEN]", "[HALF_SCREEN_SD_CH_1080p]", "[HALF_SCREEN_SD_CH_1080p]", "[HALF_SCREEN_SD_CH_1080p]", "[HALF_SCREEN_HD]", "[HALF_SCREEN_HD]", "[HALF_SCREEN_HD]", "[NO_SIGNAL_CHANNEL_MODE]", "[NO_SIGNAL_CHANNEL_MODE]", "[NO_SIGNAL_CHANNEL_MODE_720p]", "[NO_SIGNAL_CHANNEL_MODE_720p]", "[MENU_576]", "[MENU_720]", "[MENU_1080]", "[No_Channel_1]", "[NO_SIGNAL_CHANNEL_MODE]", "[TermsConditions]", "[FTI_AFTER_SW_UPGRADE]", "[FTI_AFTER_SW_UPGRADE]", "[LANGUAGE_INSTALLATION_MODE]", "[INSTALLATION_TEXT_FTI]", "[INSTALLATION_ENGLISH]", "[ENGLISH_TERMOS]", "[ENGLISH_INSTALLATION_LANGUAGE]", "[FTI_AFTER_SW_UPGRADE_OLD]", "[FTI_AFTER_SW_UPGRADE_OLD_1]", "[FTI_AFTER_SW_UPGRADE_OLD_2]", "[Inst_Success]"],
                                                                    [80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 30, 80, 80, 80, NOS_API.thres, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80])
                                        
                                if(compare_result == 0 or compare_result >= 34):
                                    NOS_API.test_cases_results_info.channel_boot_up_state = False
                                    time.sleep(2)    
                                    #test_result = "PASS"
                                    Software_Upgrade_TestCase = True
                                    #Act = 2
                                elif(compare_result >= 4 and compare_result < 11):
                                    if (Act == 0):
                                        Act = Act + 1
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                        NOS_API.set_error_message("Não Actualiza") 
                                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                        test_result = "FAIL"
                                        Repeat = 2
                                        Act = 2
                                elif(compare_result >= 11 and compare_result < 13):
                                    TEST_CREATION_API.write_log_to_file("Incorrect SW - UMA")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.Incorret_SW_UMA_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.Incorret_SW_UMA_error_message)                                        
                                    NOS_API.set_error_message("Sw Incorreto - UMA") 
                                    error_codes =  NOS_API.test_cases_results_info.Incorret_SW_UMA_error_code
                                    error_messages = NOS_API.test_cases_results_info.Incorret_SW_UMA_error_message                               
                                    test_result = "FAIL"
                                    Repeat = 2
                                    Act = 2
                                elif(compare_result >= 13 and compare_result < 34 or compare_result >= 1 and compare_result < 4):
                                    NOS_API.test_cases_results_info.channel_boot_up_state = True
                                    if(compare_result >= 1 and compare_result < 3):
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                    ## Wait to close MENU
                                    result_ch = NOS_API.wait_for_multiple_pictures(
                                                                        ["error_channel_mode_ref"],
                                                                        15,
                                                                        ["[ERROR_CHANNEL_MODE]"],
                                                                        [80])
                                    if(result_ch == -2):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 960.")
                                            Break_Cicle = True
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    if(result_ch != -1):
                                        if (Act == 0):
                                            Act = Act + 1
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                            NOS_API.set_error_message("Não Actualiza") 
                                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message 
                                            Repeat = 2
                                            Act = 2
                                    else:
                                        TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                        TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        
                                        result = NOS_API.wait_for_multiple_pictures(
                                                                            ["error_channel_mode_ref"],
                                                                            30,
                                                                            ["[ERROR_CHANNEL_MODE]"],
                                                                            [80])
                                        if(result == -2):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1028.")
                                                Break_Cicle = True
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        if(result != -1):
                                            if (Act == 0):
                                                Act = Act + 1
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                    
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                                NOS_API.set_error_message("Não Actualiza") 
                                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message  
                                                Repeat = 2
                                                Act = 2
                                        else:
                                            #test_result = "PASS"
                                            Software_Upgrade_TestCase = True
                                            #Act = 2
                                else:
                                    delta_time_standby = (time.mktime(time.localtime()) - time.mktime(start_time_standby_mode))
                                    
                                    if(delta_time_standby < SW_UPGRADE_TIMEOUT):
                                        
                                        if (NOS_API.is_signal_present_on_video_source()):  
                                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                            if not (NOS_API.grab_picture("Check_Black")):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1097.")
                                                    Break_Cicle = True
                                                    break
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return
                                            video_result = 0
                                            video_result_1 = 0
                                            if (video_height == "720"):
                                                video_result = NOS_API.compare_pictures("Black_HDMI", "Check_Black", "[FULL_SCREEN_720]")
                                            elif(video_height == "1080"):
                                                video_result_1 = NOS_API.compare_pictures("black_screen_ref", "Check_Black", "[FULL_SCREEN]")
                                            else:
                                                continue
                                            if (video_result >= 80 or video_result_1 >= 80):
                                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                time.sleep(4)
                                                continue
                                            else:
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                time.sleep(2)
                                                continue
                                        else:    
                                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                            time.sleep(4)
                                            continue
                                            
                                    result = NOS_API.wait_for_multiple_pictures(
                                            ["searching_for_sw_576_ref", "Check_Por_Favor_CVBS", "Check_Por_Favor_CVBS_1", "Check_Por_Favor_CVBS_old", "searching_for_sw_720_ref", "searching_for_sw_1080_ref"],
                                            3,
                                            ["[SEARCH_SW_HDMI_576]", "[FULL_SCREEN_576]", "[FULL_SCREEN_576]", "[FULL_SCREEN_576]", "[SEARCH_SW_HDMI_720]", "[SEARCH_SW_HDMI_1080]"],
                                            [30,30,30,30,80,80])
                                    
                                    if(result == -2):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1169.")
                                            Break_Cicle = True
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    if(result != -1):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 3
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 2
                                            TEST_CREATION_API.write_log_to_file("No boot. Line 1215.")
                                            Break_Cicle = True
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("No boot")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                            NOS_API.set_error_message("Não arranca")
                                            error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                            Repeat = 2
                                            Act = 2
                                            test_end = 0
                                    else:                            
                                        TEST_CREATION_API.write_log_to_file("Image is not reproduced correctly on HDMI.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                        NOS_API.set_error_message("Video HDMI")
                                        Repeat = 2
                                        Act = 2
                                        test_end = 0
                                
                                delta_time_standby = (time.mktime(time.localtime()) - time.mktime(start_time_standby_mode))  
                                break
                            else:
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(5)
                                if (NOS_API.is_signal_present_on_video_source()):
                                    continue
                                time.sleep(10)
                        
                        if (Break_Cicle):
                            break
                            
                        # If STB didn't power on
                        if(delta_time_standby > SW_UPGRADE_TIMEOUT and test_end != 0):
                            if not(NOS_API.is_signal_present_on_video_source()):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 3
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 2
                                    TEST_CREATION_API.write_log_to_file("No boot. Line 1250.")
                                    break
                                else:
                                    TEST_CREATION_API.write_log_to_file("No boot")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                    NOS_API.set_error_message("Não arranca")
                                    error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                                    error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                    Repeat = 2
                                    Act = 2
                            else:
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 3
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 2
                                    TEST_CREATION_API.write_log_to_file("No boot or Reboot. Line 1263.")
                                    break
                                else:
                                    TEST_CREATION_API.write_log_to_file("No boot or Reboot")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                    NOS_API.set_error_message("Não arranca")
                                    error_codes =  NOS_API.test_cases_results_info.no_boot_error_code
                                    error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                    Repeat = 2
                                    Act = 2   
    ####    ##########################################################################################################################################################################################################################    
    ####    #########################################################################################Input Signal#####################################################################################################################    
    ####    ##########################################################################################################################################################################################################################
                
                    if(Software_Upgrade_TestCase):   
                        TEST_CREATION_API.write_log_to_file("####Input Signal####")
                        if (Act == 0):
                            NOS_API.give_me_give_me_give_me_a_time_after_finish("Arranque")   
                        else:
                            NOS_API.give_me_give_me_give_me_a_time_after_finish("Atualização e Arranque")   
                        if (NOS_API.is_signal_present_on_video_source()):
        
                            ## Check state of STB
                            if (NOS_API.test_cases_results_info.channel_boot_up_state):
                                
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                time.sleep(4)
                                
                                TEST_CREATION_API.send_ir_rc_command("[MENU]")
                                
                                if not (NOS_API.grab_picture("Menu_Image")):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1315.")
                                        break
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return
                                
                                result = NOS_API.wait_for_multiple_pictures(["Menu_SW_UMA_ref", "Menu_SW_UMA_720_ref"], 5, ["[SW_UMA_Menu]", "[SW_UMA_Menu_720]"], [80, 80])
                                if(result == -2):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1505.")
                                        break
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                if (result != -1):
                                    TEST_CREATION_API.write_log_to_file("Incorrect SW - UMA")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.Incorret_SW_UMA_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.Incorret_SW_UMA_error_message)                                        
                                    NOS_API.set_error_message("Sw Incorreto - UMA") 
                                    error_codes =  NOS_API.test_cases_results_info.Incorret_SW_UMA_error_code
                                    error_messages = NOS_API.test_cases_results_info.Incorret_SW_UMA_error_message                               
                                    test_result = "FAIL"
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                            
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                                    
                                    if (Act == 0):
                                        Act = Act + 1
                                        continue
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                        NOS_API.set_error_message("Não Actualiza") 
                                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                        test_result = "FAIL"
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return
                                 
                                TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                
                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                ## Check is resolution different than 1080i
                                if (video_height != "1080"):
                                    if (video_height == "720"):
                                        TEST_CREATION_API.send_ir_rc_command("[RESOLUTION_SETTINGS]")
                                        if not (NOS_API.grab_picture("Resolution_Right_Place")):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1315.")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                        
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return
                                        comparassion_result = NOS_API.compare_pictures("Resolution_Right_Place_720_ref", "Resolution_Right_Place", "[Resolution_Right_Place_720]")
                                        if not(comparassion_result >= NOS_API.thres):
                                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            time.sleep(3)
                                            TEST_CREATION_API.send_ir_rc_command("[RESOLUTION_SETTINGS_SLOW]")
                                            if not (NOS_API.grab_picture("Resolution_Right_Place_1")):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1315.")
                                                    break
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                            
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return
                                            comparassion_result = NOS_API.compare_pictures("Resolution_Right_Place_720_ref", "Resolution_Right_Place_1", "[Resolution_Right_Place_720]")
                                            if not(comparassion_result >= NOS_API.thres):
                                                NOS_API.set_error_message("Navegação")
                                                TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                                NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                            ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                report_file = ""    
                                
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)                           
                                                            
                                                return
                                    elif (video_height == "576"):
                                        TEST_CREATION_API.send_ir_rc_command("[RESOLUTION_SETTINGS]")
                                        if not (NOS_API.grab_picture("Resolution_Right_Place")):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1315.")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                        
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return
                                        comparassion_result = NOS_API.compare_pictures("Resolution_Right_Place_576_ref", "Resolution_Right_Place", "[Resolution_Right_Place_576]")
                                        if not(comparassion_result >= NOS_API.thres):
                                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                            time.sleep(3)
                                            TEST_CREATION_API.send_ir_rc_command("[RESOLUTION_SETTINGS_SLOW]")
                                            if not (NOS_API.grab_picture("Resolution_Right_Place_1")):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1315.")
                                                    break
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                            
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return
                                            comparassion_result = NOS_API.compare_pictures("Resolution_Right_Place_576_ref", "Resolution_Right_Place_1", "[Resolution_Right_Place_576]")
                                            if not(comparassion_result >= NOS_API.thres):
                                                NOS_API.set_error_message("Navegação")
                                                TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                                NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                            ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                report_file = ""    
                                
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)                           
                                                            
                                                return
                                    TEST_CREATION_API.send_ir_rc_command("[Change_Resolution_FHD]")
                                    time.sleep(3)
                                    if not(NOS_API.is_signal_present_on_video_source()):
                                        time.sleep(2)
                                    if (NOS_API.is_signal_present_on_video_source()):
                                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                        if (video_height != "1080"):
                                            try:
                                                NOS_API.grab_picture("Debug")
                                            except:
                                                pass
                                            TEST_CREATION_API.write_log_to_file("Resolution: " + video_height)
                                            NOS_API.set_error_message("Resolução")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = ""    
                                        
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                                            return
                                    else:
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4173.")
                                            continue
                                        else:
                                            #NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal after change Resolution.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = ""    
                                        
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                                            return
                                                                                 
                                ## Check language
                                TEST_CREATION_API.send_ir_rc_command("[SETTINGS]")
                                if not(NOS_API.grab_picture("Language__")):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1460.")
                                        break
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return
                                result = NOS_API.wait_for_multiple_pictures(["settings_english_language_ref", "settings_english_language_no_signal_ref"], 5, ["[ENGLISH_LANGUAGE_DETECTED]", "[ENGLISH_LANGUAGE_DETECTED]"], [NOS_API.thres, NOS_API.thres])
                                if(result == -2):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1505.")
                                        break
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                if (result != -1): 
                                    TEST_CREATION_API.send_ir_rc_command("[LANGUAGE_SCREEN]")                    
                                    result = NOS_API.wait_for_multiple_pictures(["language_screen_ref", "language_screen_no_signal_ref", "language_screen_english_ref", "language_screen_english_no_signal_ref"], 5, ["[LANGUAGE_SCREEN]", "[LANGUAGE_SCREEN]", "[LANGUAGE_SCREEN]", "[LANGUAGE_SCREEN]"], [NOS_API.thres, NOS_API.thres, NOS_API.thres, NOS_API.thres])
                                    if(result == -2):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1554.")
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    if (result == -1):
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        time.sleep(3)
                                        TEST_CREATION_API.send_ir_rc_command("[LANGUAGE_SCREEN]") 
                                        result = NOS_API.wait_for_multiple_pictures(["language_screen_ref", "language_screen_no_signal_ref", "language_screen_english_ref", "language_screen_english_no_signal_ref"], 5, ["[LANGUAGE_SCREEN]", "[LANGUAGE_SCREEN]", "[LANGUAGE_SCREEN]", "[LANGUAGE_SCREEN]"], [NOS_API.thres, NOS_API.thres, NOS_API.thres, NOS_API.thres])
                                        if(result == -2):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1604.")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        if (result == -1):
                                            NOS_API.set_error_message("Navegação")
                                            TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                            error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = ""    
                            
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)                           
                                                        
                                            return
                                                            
                                    TEST_CREATION_API.send_ir_rc_command("[SET_PORTUGAL_FROM_LANGUAGE_SCREEN]")
        
                                TEST_CREATION_API.send_ir_rc_command("[Check_Upgrade]")
                                result = NOS_API.wait_for_multiple_pictures(["sw_version_ref", "sw_version_black_ref", "sw_version_ref_old", "sw_version_ref_old_1"], 5, ["[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN_Two]", "[SW_VERSION_SCREEN_Two]"], [NOS_API.thres_1, NOS_API.thres_1, NOS_API.thres_1, NOS_API.thres_1])
                                if(result == -2):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1693.")
                                        break
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                if (result == -1):
                                    if not(NOS_API.grab_picture("STB_Version_First_Navigation")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1740.")
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    time.sleep(3)
                                    TEST_CREATION_API.send_ir_rc_command("[Check_Upgrade_Scnd]") 
                                    result = NOS_API.wait_for_multiple_pictures(["sw_version_ref", "sw_version_black_ref", "sw_version_ref_old"], 5, ["[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN_Two]"], [NOS_API.thres_1, NOS_API.thres_1, NOS_API.thres_1])
                                    if(result == -2):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1787.")
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    if (result == -1):
                                        time.sleep(1)
                                        if not(NOS_API.grab_picture("STB_Version_Second_Navigation")):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1835.")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place or doesn't appear STB Info.")
                                        NOS_API.set_error_message("Navegação")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                        NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                    ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""    
                        
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)                           
                                                    
                                        return
                                if(result == 3):
                                    if (Act == 0 and NOS_API.Upgrade_State == 0):
                                        Act = Act + 1
                                        continue
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                        NOS_API.set_error_message("Não Actualiza") 
                                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message 
                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""    
                        
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                        
                                        return
                                if not(NOS_API.grab_picture("STB_Version")):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1960.")
                                        break
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return
                                ## Get IRIS version from menu
                                iris_version = TEST_CREATION_API.OCR_recognize_text("STB_Version", "[IRIS_VERSION]", "[OCR_FILTER]")
                                NOS_API.test_cases_results_info.iris_version = iris_version
                                TEST_CREATION_API.write_log_to_file("IRIS version: " + iris_version)
                                NOS_API.update_test_slot_comment("IRIS version: " + iris_version)
                                ## Get SoftWare version from menu
                                sw_version = TEST_CREATION_API.OCR_recognize_text("STB_Version", "[SOFTWARE_VERSION]", "[OCR_FILTER]", "sw_version")
                                TEST_CREATION_API.write_log_to_file("The extracted sc version is: " + sw_version)
                                NOS_API.update_test_slot_comment("SW version: " + NOS_API.test_cases_results_info.firmware_version)
                                NOS_API.test_cases_results_info.firmware_version = str(sw_version)
                                
                                if not(sw_version == sw_version_prod and iris_version == iris_version_prod): 
                                    if (Act == 0 and NOS_API.Upgrade_State == 0):
                                        Act = Act + 1
                                        continue
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                        NOS_API.set_error_message("Não Actualiza") 
                                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message 
                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""    
                        
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                        
                                        return
                                
                                TEST_CREATION_API.send_ir_rc_command("[SIGNAL_VALUE_NEW_Ch]")
                                result = NOS_API.wait_for_multiple_pictures(["rede_screen_ref", "rede_screen_no_signal_ref"], 5, ["[REDE_SCREEN]", "[REDE_SCREEN]"], [NOS_API.thres, NOS_API.thres])
                                if(result == -2):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2059.")
                                        break
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                        
                                        return
                                if (result == -1):
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                    TEST_CREATION_API.send_ir_rc_command("[SIGNAL_VALUE_NEW]")
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                    time.sleep(2)
                                    result = NOS_API.wait_for_multiple_pictures(["rede_screen_ref", "rede_screen_no_signal_ref"], 5, ["[REDE_SCREEN]", "[REDE_SCREEN]"], [NOS_API.thres, NOS_API.thres])
                                    if(result == -2):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2112.")
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    if (result == -1):
                                        TEST_CREATION_API.write_log_to_file("Navigation to rede screen failed")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                        NOS_API.set_error_message("Navegação")
                                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""    
                        
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                        
                                        return
                                        
                                ## OCR macros
                                macro_snr =  "[SNR_CHANNEL_BOOT_UP_STATE_1]" # if write: POWER: xdbmV
                                macro_ber =  "[BER_CHANNEL_BOOT_UP_STATE]"
                                
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                time.sleep(2)
                            else:
                                
                                ## Navigate to the FTI
                                TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_FTI_SCREEN]")
        
                        
                                ## OCR macros
                                macro_snr =  "[SNR_INSTALLATION_BOOT_UP_STATE_1]"
                                macro_ber =  "[BER_INSTALLATION_BOOT_UP_STATE]"
                            
                            if (NOS_API.grab_picture("signal_value")):
                                if not(NOS_API.test_cases_results_info.channel_boot_up_state):   
                                    right_place_result = NOS_API.wait_for_multiple_pictures(["installation_boot_up_ref", "installation_boot_up_ref1", "installation_boot_up_ref_old", "english_installation", "Installation_Check_Signal", "No_Signal_Installation_ref"], 5, ["[Installation_Check_Signal]", "[Installation_Check_Signal]", "[Installation_Check_Signal]", "[Installation_Check_Signal]", "[Installation_Check_Signal]", "[Installation_Check_Signal]"], [80, 80, 80, 80, 80, 80])       
                                    if(right_place_result == -2):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2216.")
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            test_result = "FAIL"
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                            
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                            
                                            return
                                    if (right_place_result == -1):   
                                        ## Navigate to the FTI
                                        TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_FTI_SCREEN]")                
                                        right_place_result = NOS_API.wait_for_multiple_pictures(["installation_boot_up_ref", "installation_boot_up_ref_old", "english_installation", "Installation_Check_Signal", "No_Signal_Installation_ref"], 5, ["[Installation_Check_Signal]", "[Installation_Check_Signal]", "[Installation_Check_Signal]", "[Installation_Check_Signal]", "[Installation_Check_Signal]"], [80, 80, 80, 80, 80])
                                        if(right_place_result == -2):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2266.")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                
                                                return
                                        if (right_place_result == -1):
                                            NOS_API.set_error_message("Navegação")
                                            TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                            error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = ""    
                            
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)                           
                                                        
                                            return                        
                                        if not(NOS_API.grab_picture("signal_value")):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2350.")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return
                                try:             
                                    
                                    ## Extract snr text from image
                                    snr_value = NOS_API.fix_snr_power(NOS_API.replace_letter_o_with_number_0(TEST_CREATION_API.OCR_recognize_text("signal_value", macro_snr, "[OCR_FILTER]")))  ## POWER text
                                    TEST_CREATION_API.write_log_to_file("Snr value: " + snr_value)
                                    NOS_API.update_test_slot_comment("Snr value: " + snr_value)
                                
                                    snr_value = float(snr_value[:(snr_value.find('d'))])
                                    
                                    NOS_API.test_cases_results_info.power = str(snr_value)
                                    
                                    if (snr_value <= SNR_VALUE_THRESHOLD_LOW or snr_value >= SNR_VALUE_THRESHOLD_HIGH):
                                        
                                        time.sleep(2)                        
                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                        NOS_API.display_custom_dialog("Confirme Cabo RF e restantes cabos", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        time.sleep(5)
                                        if (NOS_API.grab_picture("signal_value")):
        
                                            try:             
                                                
                                                ## Extract snr text from image
                                                snr_value = NOS_API.fix_snr_power(NOS_API.replace_letter_o_with_number_0(TEST_CREATION_API.OCR_recognize_text("signal_value", macro_snr, "[OCR_FILTER]")))  ## POWER text
                                                #snr_value = NOS_API.fix_snr_power(TEST_CREATION_API.OCR_recognize_text("signal_value", macro_snr, "[OCR_FILTER]"))  ## POWER text
                                                TEST_CREATION_API.write_log_to_file("Snr value: " + snr_value)
                                                NOS_API.update_test_slot_comment("Snr value: " + snr_value)
                                            
                                                snr_value = float(snr_value[:(snr_value.find('d'))])
                                                
                                                NOS_API.test_cases_results_info.power = str(snr_value)
                                                    
                                                
                                            except Exception as error:
                                                ## Set test result to INCONCLUSIVE
                                                TEST_CREATION_API.write_log_to_file(str(error))
                                                snr_value = 0
                                                NOS_API.test_cases_results_info.power = "-"
                                            
                                        else:
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2388.")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return
                                
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    snr_value = 0
                                    NOS_API.test_cases_results_info.power = "-"        
                                                
                                try:
                                    ## Extract ber text from image
                                    ber_value = TEST_CREATION_API.OCR_recognize_text("signal_value", macro_ber, "[OCR_FILTER]", "BER_Value")
                                    ber_value = NOS_API.fix_ber(ber_value)
                                    TEST_CREATION_API.write_log_to_file("BER value: " + ber_value)
                                    NOS_API.update_test_slot_comment("BER value: " + ber_value)
                                    NOS_API.test_cases_results_info.ber = str(ber_value)
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    ber_value = "-"
                                    NOS_API.test_cases_results_info.ber = "-"
                                    
                                if (NOS_API.test_cases_results_info.channel_boot_up_state):
                                    try:
                                        frequencia = TEST_CREATION_API.OCR_recognize_text("signal_value", "[FREQUENCIA]", "[OCR_FILTER]")
                                        NOS_API.test_cases_results_info.freq = str(frequencia)
                                        modulation = TEST_CREATION_API.OCR_recognize_text("signal_value", "[MODULATION]", "[OCR_FILTER]")
                                        NOS_API.test_cases_results_info.modulation = str(modulation)
                                        NOS_API.update_test_slot_comment("Frequencia: " + frequencia)
                                        NOS_API.update_test_slot_comment("Modulation: " + modulation)
                                    except Exception as error:
                                        ## Set test result to INCONCLUSIVE
                                        TEST_CREATION_API.write_log_to_file(str(error))
                                
                                ## Check if snr value higher than threshold
                                if (snr_value > SNR_VALUE_THRESHOLD_LOW and snr_value < SNR_VALUE_THRESHOLD_HIGH):
                                    ## Check if ber value higher than threshold
                                    if (NOS_API.check_ber(ber_value, BER_VALUE_THRESHOLD)):
                                        #test_result = "PASS"
                                        Input_Signal_TestCase = True
                                        
                                        if not(NOS_API.test_cases_results_info.channel_boot_up_state):      
                                        
                                            TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                            time.sleep(2)
                                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                                            TEST_CREATION_API.send_ir_rc_command("[UP]")
                                            TEST_CREATION_API.send_ir_rc_command("[OK]") 
                                            
                                            result = NOS_API.wait_for_multiple_pictures(["error_instalation_mode_ref", "error_instalation_mode_ref_old"], 5, ["[ERROR_INSTALLATION_MODE]", "[ERROR_INSTALLATION_MODE]"], [80, 80])
                                            if(result == -2):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2480.")
                                                    break
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return
                                            if (result != -1):
                                                if (Act == 0 and NOS_API.Upgrade_State == 0):
                                                    Act = Act + 1
                                                    continue
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                                    NOS_API.set_error_message("Não Actualiza") 
                                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                                    
                                                    test_result = "FAIL"
        
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        str(snr_value) + " " + str(ber_value) + " - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    report_file = ""    
                                    
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                    
                                                    return                                                                                                                                               
                                            
                                            ch_installation_fti = False                            
                                            result = NOS_API.wait_for_multiple_pictures(["channel_installation_fti_finished_ref"], 110, ["[CHANNEL_INSTALLATION_FINISH_FTI]"], [80])
                                            if(result == -2):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2574.")
                                                    break
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return
                                            if (result == -1):
                                                result = NOS_API.wait_for_multiple_pictures(["channel_installtion_failed_ref"], 3, ["[CHANNEL_INSTALLATION_FINISH_FTI]"], [80])
                                                if(result == -2):
                                                    if (Repeat == 0):
                                                        Repeat = Repeat + 1
                                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                                        else:
                                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2622.")
                                                        break
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                        
                                                        return
                                                if (result != -1):
                                                    TEST_CREATION_API.write_log_to_file("STB lost RF signal in the middle of channel installation")
                        
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                                                    NOS_API.set_error_message("SNR")
                                                    error_codes = NOS_API.test_cases_results_info.snr_error_code
                                                    error_messages = NOS_API.test_cases_results_info.snr_error_message
                                                    test_result = "FAIL"
                                                    Input_Signal_TestCase = False
                                                    Repeat = 2
                                                    Act = 2
                                                else:
                                                    TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_FTI_SCREEN]")
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_SIGNAL_VALUE_SCREEN_INSTALLATION_BOOT_UP_1_NEW]")
                                                    result = NOS_API.wait_for_multiple_pictures(["channel_installation_fti_finished_ref"], 110, ["[CHANNEL_INSTALLATION_FINISH_FTI]"], [80])
                                                    if(result == -2):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2684.")
                                                            break
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            test_result = "FAIL"
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = ""
                                                            if (test_result != "PASS"):
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                            
                                                            return
                                                    if (result == -1):
                                                        if not (NOS_API.grab_picture("STB_BLOCKS")):
                                                            if (Repeat == 0):
                                                                Repeat = Repeat + 1
                                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                                else:
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2731.")
                                                                break
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                                NOS_API.set_error_message("Reboot")
                                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                                
                                                                NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                
                                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                            
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                                        
                                                                NOS_API.send_report_over_mqtt_test_plan(
                                                                        test_result,
                                                                        end_time,
                                                                        error_codes,
                                                                        report_file)
                                                                        
                                                                ## Update test result
                                                                TEST_CREATION_API.update_test_result(test_result)
                                                                
                                                                ## Return DUT to initial state and de-initialize grabber device
                                                                NOS_API.deinitialize()
                                                                
                                                                return
                                                        if(TEST_CREATION_API.compare_pictures("Installatio_Blocks_ref", "STB_BLOCKS")):                                       
                                                            TEST_CREATION_API.write_log_to_file("STB Blocks")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.block_error_message)
                                                            NOS_API.set_error_message("STB bloqueou")
                                                            error_codes = NOS_API.test_cases_results_info.block_error_code
                                                            error_messages = NOS_API.test_cases_results_info.block_error_message
                                                            test_result = "FAIL"
                                                            Input_Signal_TestCase = False
                                                            Repeat = 2
                                                            Act = 2
                                                        else:
                                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                                                            NOS_API.set_error_message("IR")
                                                            error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                                            error_messages = NOS_API.test_cases_results_info.ir_nok_error_message   
                                                            TEST_CREATION_API.write_log_to_file("STB didn't receive RCU Comands")
                                                            test_result = "FAIL"
                                                            Input_Signal_TestCase = False
                                                            Repeat = 2
                                                            Act = 2
                                                    else:
                                                        ch_installation_fti = True
                                            else:
                                                ch_installation_fti = True
                                            
                                            if (ch_installation_fti == True):
                                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                                time.sleep(2)
                                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                                time.sleep(30)
                                                
                                                TEST_CREATION_API.send_ir_rc_command("[BACK]")
                                                time.sleep(3)
                                                
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                time.sleep(4)              
                                                
                                                TEST_CREATION_API.send_ir_rc_command("[Check_Upgrade_Inst]")
                                                result = NOS_API.wait_for_multiple_pictures(["sw_version_ref", "sw_version_black_ref", "sw_version_ref_old"], 5, ["[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN_Two]"], [NOS_API.thres_1, NOS_API.thres_1, NOS_API.thres_1])
                                                if(result == -2):
                                                    if (Repeat == 0):
                                                        Repeat = Repeat + 1
                                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                                        else:
                                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2816.")
                                                        break
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                        
                                                        return
                                                if (result == -1):
                                                    if not(NOS_API.grab_picture("wrong_navigation")):
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                
                                                        return
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                    time.sleep(3)
                                                    TEST_CREATION_API.send_ir_rc_command("[Check_Upgrade_Scnd]") 
                                                    result = NOS_API.wait_for_multiple_pictures(["sw_version_ref" , "sw_version_black_ref", "sw_version_ref_old"], 5, ["[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN]", "[SW_VERSION_SCREEN_Two]"], [NOS_API.thres_1, NOS_API.thres_1, NOS_API.thres_1])
                                                    if(result == -2):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2866.")
                                                            break
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            test_result = "FAIL"
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = ""
                                                            if (test_result != "PASS"):
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                            
                                                            return
                                                    if (result == -1):
                                                        TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                        NOS_API.set_error_message("Navegação")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                                        test_result = "FAIL"
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                                    test_result,
                                                                                    "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                                                    ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                                    error_codes,
                                                                                    error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = ""    
                                        
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)                           
                                                                    
                                                        return
                                                if not(NOS_API.grab_picture("STB_Version")):
                                                    if (Repeat == 0):
                                                        Repeat = Repeat + 1
                                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                                        else:
                                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 2951.")
                                                        break
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                        
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                    
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                                
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                                
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        return
                                                ## Get IRIS version from menu
                                                iris_version = TEST_CREATION_API.OCR_recognize_text("STB_Version", "[IRIS_VERSION]", "[OCR_FILTER]")
                                                NOS_API.test_cases_results_info.iris_version = iris_version
                                                TEST_CREATION_API.write_log_to_file("IRIS version: " + iris_version)
                                                NOS_API.update_test_slot_comment("IRIS version: " + iris_version)
                                                ## Get SoftWare version from menu
                                                sw_version = TEST_CREATION_API.OCR_recognize_text("STB_Version", "[SOFTWARE_VERSION]", "[OCR_FILTER]", "sw_version")
                                                TEST_CREATION_API.write_log_to_file("The extracted sc version is: " + sw_version)
                                                NOS_API.update_test_slot_comment("SW version: " + NOS_API.test_cases_results_info.firmware_version)
                                                NOS_API.test_cases_results_info.firmware_version = str(sw_version)
                                                
                                                if not(sw_version == sw_version_prod and iris_version == iris_version_prod): 
                                                    if (Act == 0 and NOS_API.Upgrade_State == 0):
                                                        Act = Act + 1
                                                        continue
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                                        NOS_API.set_error_message("Não Actualiza") 
                                                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message 
                                                        test_result = "FAIL"
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                                        test_result,
                                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                                        ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                                                        error_codes,
                                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = ""    
                                        
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                        
                                                        return
        
                                                ## Navigate to the screen to check frequency and modulation
                                                TEST_CREATION_API.send_ir_rc_command("[SIGNAL_VALUE_NEW_Ch]")
                                            
                                                result = NOS_API.wait_for_multiple_pictures(["rede_screen_ref", "rede_screen_no_signal_ref"], 5, ["[REDE_SCREEN]", "[REDE_SCREEN]"], [NOS_API.thres, NOS_API.thres])
                                                if(result == -2):
                                                    if (Repeat == 0):
                                                        Repeat = Repeat + 1
                                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                                        else:
                                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3053.")
                                                        break
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                        
                                                        return
                                                if (result == -1):
                                                    if not(NOS_API.grab_picture("Wrong_Navigation_Rede")):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3100.")
                                                            break
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                        
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                                    
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                                                    
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            return
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                                    TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                    time.sleep(7)
                                                    TEST_CREATION_API.send_ir_rc_command("[SIGNAL_VALUE_NEW]")
                                                    result = NOS_API.wait_for_multiple_pictures(["rede_screen_ref"], 5, ["[REDE_SCREEN]"], [NOS_API.thres])
                                                    if(result == -2):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3148.")
                                                            break
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            test_result = "FAIL"
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = ""
                                                            if (test_result != "PASS"):
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                            
                                                            return
                                                    if (result == -1):
                                                        test_result = "FAIL"
                                                        TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                                        NOS_API.set_error_message("Navegação")
                                                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = ""    
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                                        
                                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        return
                                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                time.sleep(2)
                                                if (NOS_API.grab_picture("freq_mod")):    
                                                    try:
                                                        frequencia = TEST_CREATION_API.OCR_recognize_text("freq_mod", "[FREQUENCIA]", "[OCR_FILTER]")
                                                        NOS_API.test_cases_results_info.freq = str(frequencia)
                                                        modulation = TEST_CREATION_API.OCR_recognize_text("freq_mod", "[MODULATION]", "[OCR_FILTER]")
                                                        NOS_API.test_cases_results_info.modulation = str(modulation)
                                                        NOS_API.update_test_slot_comment("Frequencia: " + frequencia)
                                                        NOS_API.update_test_slot_comment("Modulation: " + modulation)
                                                    except Exception as error:
                                                        ## Set test result to INCONCLUSIVE
                                                        TEST_CREATION_API.write_log_to_file(str(error))
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    test_result = "FAIL"
                                                    Input_Signal_TestCase = False
                                                    Repeat = 2
                                                    Act = 2
                                        
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_SIGNAL_VALUE_SCREEN_CHANNEL_BOOT_UP_NEW]")
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_SIGNAL_VALUE_SCREEN_CHANNEL_BOOT_UP_NEW2]")
                                        Act = 2
                                    else:
                                        TEST_CREATION_API.write_log_to_file("BER value is lower than threshold")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ber_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.ber_error_message)
                                        NOS_API.set_error_message("BER") 
                                        
                                        error_codes = NOS_API.test_cases_results_info.ber_error_code
                                        error_messages = NOS_API.test_cases_results_info.ber_error_message
                                        Repeat = 2
                                        Act = 2
                                else:
                                    TEST_CREATION_API.write_log_to_file("SNR value is lower than threshold")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                                    NOS_API.set_error_message("SNR")
                                    error_codes = NOS_API.test_cases_results_info.snr_error_code
                                    error_messages = NOS_API.test_cases_results_info.snr_error_message
                                    Repeat = 2
                                    Act = 2
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message  
                                Repeat = 2
                                Act = 2
                        else:
                            #NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                            NOS_API.set_error_message("Reboot")
                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                            Repeat = 2
                            Act = 2

                if (NOS_API.test_cases_results_info.DidUpgrade == 1):
                    #if not(NOS_API.change_usb_port("USBHUB-10##")):
                    NOS_API.Send_Serial_Key("d", "feito")
            ##############################################################################################################################################################################################################################    
            #############################################################################################Serial Number####################################################################################################################    
            ##############################################################################################################################################################################################################################
                    
                if(Input_Signal_TestCase): 
                    TEST_CREATION_API.write_log_to_file("####Serial Number####")
                    NOS_API.give_me_give_me_give_me_a_time_after_finish("Instalação Canais / Verificação de Sinal / Versão SW")   
                        
                    RX_THRESHOLD_LOW = -20
                    RX_THRESHOLD_HIGH = 20
                    ########### CHANGE #############
                    TX_THRESHOLD = 60
                    DOWNLOADSTREAM_SNR_THRESHOLD = 20
        
                    ## Set test result default to FAIL
                    test_result = "FAIL"
                    
                    error_codes = ""
                    error_messages = ""
                    
                    sw_version_prod = NOS_API.Firmware_Version_DCR_8151
                    iris_version_prod = NOS_API.IRIS_Version_DCR_8151
        
                    if (NOS_API.is_signal_present_on_video_source()):
        
                        TEST_CREATION_API.send_ir_rc_command("[Change_to_FTTH_First]")
                        result = NOS_API.wait_for_multiple_pictures(["Conectividade_black_ref", "Conectividade_ref"], 5, ["[Conectividade]", "[Conectividade]"], [NOS_API.thres_1, NOS_API.thres_1])
                        if(result == -2):
                            if (Repeat == 0):
                                Repeat = Repeat + 1
                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3330.")
                                continue
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
            
            
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
            
                                return
                        if(result == -1):
                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                            time.sleep(3)
                            TEST_CREATION_API.send_ir_rc_command("[Change_to_FTTH_Scnd]")
                            result = NOS_API.wait_for_multiple_pictures(["Conectividade_black_ref", "Conectividade_ref"], 5, ["[Conectividade]", "[Conectividade]"], [NOS_API.thres_1, NOS_API.thres_1])
                            if(result == -2):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3380.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                    
                                    return
                            if(result == -1):
                                TEST_CREATION_API.write_log_to_file("Navigation to Conectivity screen failed")
                                
                                NOS_API.set_error_message("Navegação")
                                
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - " + str(tx_value) + " " + str(rx_value) + " " + str(downloadstream_snr_value) + " - - - - - " + str(cas_id_number) + " " + str(sw_version) + " - " + str(sc_number) + " - - - -",
                                            "- - - - <52 >-10<10 >=34 - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
        
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return
                        
                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                        
                        TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_MODEM_DOCSIS_NEW2]")
                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                        
                        #MAC_SCREEN
                        result = NOS_API.wait_for_multiple_pictures(["mac_screen_ref", "mac_screen_ref1"], 10, ["[MAC_SCREEN]", "[MAC_SCREEN]"], [NOS_API.thres_1, NOS_API.thres_1])
                        if (result == -2):
                            if (Repeat == 0):
                                Repeat = Repeat + 1
                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3474.")
                                continue
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
            
            
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
            
                                return
                        if (result == -1):
                            if not(NOS_API.grab_picture("wrong_navigation")):
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
        
        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
        
                                return
                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                            TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                            time.sleep(3)
                            TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_MODEM_DOCSIS]")
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                            
                            result = NOS_API.wait_for_multiple_pictures(["mac_screen_ref", "mac_screen_ref1"], 10, ["[MAC_SCREEN]", "[MAC_SCREEN]"], [NOS_API.thres_1, NOS_API.thres_1])
                            if (result == -2):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3526.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
            
            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
            
                                    return
                            if (result == -1):
                                TEST_CREATION_API.write_log_to_file("Navigation to MAC screen failed")
                                
                                NOS_API.set_error_message("Navegação")
                                
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - " + str(tx_value) + " " + str(rx_value) + " " + str(downloadstream_snr_value) + " - - - - - " + str(cas_id_number) + " " + str(sw_version) + " - " + str(sc_number) + " - - - -",
                                            "- - - - <52 >-10<10 >=34 - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
        
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return
                
                        if (NOS_API.grab_picture("mac")):
                    
                            try:
                        
                                ## Get MAC address from menu
                                mac_number = NOS_API.fix_mac_stb_pace(NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("mac", "[MAC]", "[OCR_FILTER]")))
                                NOS_API.test_cases_results_info.mac_number = mac_number
                                TEST_CREATION_API.write_log_to_file("Mac number: " + mac_number)
                                NOS_API.update_test_slot_comment("Mac number: " + mac_number)
                            except Exception as error:
                                ## Set test result to INCONCLUSIVE
                                TEST_CREATION_API.write_log_to_file(str(error))
                                mac_number = ""
                        
                            ## Navigate to the Resumo menu
                            TEST_CREATION_API.send_ir_rc_command("[RESUMO_FROM_MODEM_DOCSIS]")
                            
                            result = NOS_API.wait_for_multiple_pictures(["resumo_ref", "resumo_ref1"], 10, ["[RESUMO]", "[RESUMO]"], [NOS_API.thres_1, NOS_API.thres_1])
                            if (result == -2):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3631.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
            
            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
            
                                    return
                            if (result == -1):
                                TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                time.sleep(3)
                                TEST_CREATION_API.send_ir_rc_command("[RESUMO]")
        
                                result = NOS_API.wait_for_multiple_pictures(["resumo_ref", "resumo_ref1"], 10, ["[RESUMO]", "[RESUMO]"], [NOS_API.thres_1, NOS_API.thres_1])
                                if (result == -2):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3682.")
                                        continue
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        test_result = "FAIL"
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
            
                                        return
                                if (result == -1):
                                    TEST_CREATION_API.write_log_to_file("Navigation to resumo screen failed")
                                    
                                    NOS_API.set_error_message("Navegação")
                                    
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                    error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                    error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                    NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - " + str(tx_value) + " " + str(rx_value) + " " + str(downloadstream_snr_value) + " - - - - - " + str(cas_id_number) + " " + str(sw_version) + " - " + str(sc_number) + " - - - -",
                                            "- - - - <52 >-10<10 >=34 - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                                
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = ""    
                                    
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
        
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
        
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    return
                        
                            ## Perform grab picture
                            if (NOS_API.grab_picture("resumo")):                                 
                                
                                try:
                                    ## Get IP address from menu
                                    ip_adress = NOS_API.replace_missed_chars_with_numbers(TEST_CREATION_API.OCR_recognize_text("resumo", "[IP_ADDRESS]", "[OCR_FILTER]"))
                                    TEST_CREATION_API.write_log_to_file("IP address: " + ip_adress)
                                    NOS_API.update_test_slot_comment("IP address: " + ip_adress)
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    ip_adress = ""
                                    
                                try:
                                    ## Get RX value from menu
                                    rx_value = TEST_CREATION_API.OCR_recognize_text("resumo", "[RX_VALUE]", "[OCR_FILTER]")
                                    NOS_API.test_cases_results_info.rx_value = rx_value
                                    TEST_CREATION_API.write_log_to_file("RX value: " + rx_value)
                                    NOS_API.update_test_slot_comment("RX value: " + rx_value)
                                    
                                    ## Extract only digits from RX value
                                    rx_value = float(NOS_API.replace_letter_o_with_number_0(rx_value[:(rx_value.find('d'))]))
                                    NOS_API.test_cases_results_info.rx = str(rx_value)
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    rx_value = -100
                                    NOS_API.test_cases_results_info.rx = "-"
                                    
                                try:
                                    ## Get download stream snr value from menu
                                    downloadstream_snr_value = TEST_CREATION_API.OCR_recognize_text("resumo", "[DOWNLOADSTREAM_SNR]", "[OCR_FILTER]")
                                    TEST_CREATION_API.write_log_to_file("Downloadstream snr value: " + downloadstream_snr_value)
                                    NOS_API.update_test_slot_comment("Downloadstream snr value: " + downloadstream_snr_value)
                                    
                                    ## Extract only digits from RX value
                                    downloadstream_snr_value = float(NOS_API.replace_letter_o_with_number_0(downloadstream_snr_value[:(downloadstream_snr_value.find('d'))]))
                                    NOS_API.test_cases_results_info.download_stream_snr = str(downloadstream_snr_value)
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    downloadstream_snr_value = 30
                                    NOS_API.test_cases_results_info.download_stream_snr = "-"
                            
                                try:
                                    ## Get TX value from menu
                                    tx_value = TEST_CREATION_API.OCR_recognize_text("resumo", "[TX_VALUE]", "[OCR_FILTER]")
                                    TEST_CREATION_API.write_log_to_file("TX value: " + str(tx_value))
                                    NOS_API.update_test_slot_comment("TX value: " + str(tx_value))
                                    
                                    ## Extract only digits from TX value
                                    tx_value = float(NOS_API.replace_letter_o_with_number_0(tx_value[:(tx_value.find('d'))]))
                                    NOS_API.test_cases_results_info.tx = str(tx_value)
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    tx_value = 0
                                    NOS_API.test_cases_results_info.tx = "-"
                                
                                mac_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.mac_using_barcode)
                                
                                ## Compare mac address from menu with previously scanned mac address
                                if (NOS_API.ignore_zero_letter_o_during_comparation(mac_number, mac_using_barcode)):
                                    if (tx_value < TX_THRESHOLD):
                                        if (rx_value > RX_THRESHOLD_LOW and rx_value < RX_THRESHOLD_HIGH):
                                            if(downloadstream_snr_value >= DOWNLOADSTREAM_SNR_THRESHOLD):
                                                if(ip_adress == "0.0.0.0"):
                                                    NOS_API.display_dialog("Confirme o cabo Eth e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                                    
                                                    time.sleep(10)
                                                    
                                                    result = NOS_API.wait_for_multiple_pictures(["resumo_ref", "resumo_ref1"], 10, ["[RESUMO]", "[RESUMO]"], [NOS_API.thres_1, NOS_API.thres_1])
                                                    if (result == -2):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3631.")
                                                            continue
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            test_result = "FAIL"
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = ""
                                                            if (test_result != "PASS"):
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                    
                                                            return
                                                    if (result == -1):
                                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                        time.sleep(3)
                                                        TEST_CREATION_API.send_ir_rc_command("[RESUMO]")
                                
                                                        result = NOS_API.wait_for_multiple_pictures(["resumo_ref", "resumo_ref1"], 10, ["[RESUMO]", "[RESUMO]"], [NOS_API.thres_1, NOS_API.thres_1])
                                                        if (result == -2):
                                                            if (Repeat == 0):
                                                                Repeat = Repeat + 1
                                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                                else:
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3682.")
                                                                continue
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                                NOS_API.set_error_message("Reboot")
                                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                                test_result = "FAIL"
                                                                
                                                                NOS_API.add_test_case_result_to_file_report(
                                                                                test_result,
                                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                                error_codes,
                                                                                error_messages)
                                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                                report_file = ""
                                                                if (test_result != "PASS"):
                                                                    report_file = NOS_API.create_test_case_log_file(
                                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                    end_time)
                                                                    NOS_API.upload_file_report(report_file)
                                                                    NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                                                ## Update test result
                                                                TEST_CREATION_API.update_test_result(test_result)
                                                                
                                                                ## Return DUT to initial state and de-initialize grabber device
                                                                NOS_API.deinitialize()
                                                                
                                                                NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                    
                                                                return
                                                        if (result == -1):
                                                            TEST_CREATION_API.write_log_to_file("Navigation to resumo screen failed")
                                                            
                                                            NOS_API.set_error_message("Navegação")
                                                            
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                            error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - " + str(tx_value) + " " + str(rx_value) + " " + str(downloadstream_snr_value) + " - - - - - " + str(cas_id_number) + " " + str(sw_version) + " - " + str(sc_number) + " - - - -",
                                                                    "- - - - <52 >-10<10 >=34 - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                        
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                            report_file = ""    
                                                            
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            return

                                                    ## Perform grab picture
                                                    if not(NOS_API.grab_picture("Eth")):
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message  
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                
                                                        return
                                                    
                                                    try:
                                                        ## Get IP address from menu
                                                        ip_adress = NOS_API.replace_missed_chars_with_numbers(TEST_CREATION_API.OCR_recognize_text("Eth", "[IP_ADDRESS]", "[OCR_FILTER]"))
                                                        TEST_CREATION_API.write_log_to_file("IP address_2: " + ip_adress)
                                                        NOS_API.update_test_slot_comment("IP address: " + ip_adress)
                                                    except Exception as error:
                                                        ## Set test result to INCONCLUSIVE
                                                        TEST_CREATION_API.write_log_to_file(str(error))
                                                        ip_adress = ""
                                                  
                                                if(ip_adress != "0.0.0.0"):
                                                    ## Navigate to the CAS ID
                                                    #TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_SC_MENU_FROM_INFO_ZON_BOX_MENU]")
                                                    TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_DOWN]")
                                                
                                                    ## Perform grab picture
                                                    if not(NOS_API.grab_picture("sc_info")):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3839.")
                                                            continue
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                        
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                                    
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                                                    
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            return
                                                
                                                    comp_result = NOS_API.compare_pictures("sc_info_ref1", "sc_info", "[CAS_ID_Place]")
                                                    comp_result1 = NOS_API.compare_pictures("sc_info_ref2", "sc_info", "[CAS_ID_Place]")
                                                    comp_result2 = NOS_API.compare_pictures("sc_info_ref3", "sc_info", "[CAS_ID_Place]")
                                                    comp_result3 = NOS_API.compare_pictures("sc_info_ref4", "sc_info", "[CAS_ID_Place]")
                                                    Flag = 0
                                                    initial_time = time.localtime()
                                                    current_time = 0
                                                    timeout_time = 60
                                                    while (comp_result < NOS_API.thres and comp_result1 < NOS_API.thres and comp_result2 < NOS_API.thres and comp_result3 < NOS_API.thres and current_time < timeout_time):
                                                        TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_DOWN]")
                                                        
                                                        ## Perform grab picture
                                                        if not(NOS_API.grab_picture("sc_info")):
                                                            if (Repeat == 0):
                                                                Repeat = Repeat + 1
                                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                                else:
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3839.")
                                                                Flag = 1
                                                                break
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                                NOS_API.set_error_message("Reboot")
                                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                                
                                                                NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                
                                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                            
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                                        
                                                                NOS_API.send_report_over_mqtt_test_plan(
                                                                        test_result,
                                                                        end_time,
                                                                        error_codes,
                                                                        report_file)
                                                                        
                                                                ## Update test result
                                                                TEST_CREATION_API.update_test_result(test_result)
                                                                
                                                                ## Return DUT to initial state and de-initialize grabber device
                                                                NOS_API.deinitialize()
                                                                
                                                                return
                                                                                    
                                                        comp_result = NOS_API.compare_pictures("sc_info_ref1", "sc_info", "[CAS_ID_Place]")
                                                        comp_result1 = NOS_API.compare_pictures("sc_info_ref2", "sc_info", "[CAS_ID_Place]")
                                                        comp_result2 = NOS_API.compare_pictures("sc_info_ref3", "sc_info", "[CAS_ID_Place]")
                                                        comp_result3 = NOS_API.compare_pictures("sc_info_ref4", "sc_info", "[CAS_ID_Place]")

                                                        # Get current time and check is testing finished
                                                        current_time = (time.mktime(time.localtime()) - time.mktime(initial_time)) 
                                                    TEST_CREATION_API.write_log_to_file("current: " + str(current_time) + "\ntimeout: " + str(timeout_time))
                                                    if current_time > timeout_time:
                                                        TEST_CREATION_API.write_log_to_file("Navigation to resumo screen failed")
                                                        
                                                        NOS_API.set_error_message("Navegação")
                                                        
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - " + str(tx_value) + " " + str(rx_value) + " " + str(downloadstream_snr_value) + " - - - - - " + str(cas_id_number) + " " + str(sw_version) + " - " + str(sc_number) + " - - - -",
                                                                "- - - - <52 >-10<10 >=34 - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                    
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = ""    
                                                        
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                            
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                            
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        return
                                                    
                                                    if (Flag == 1):
                                                        continue
                                                    
                                                    video_result1 = NOS_API.compare_pictures("sc_info_ref1", "sc_info", "[SC]")
                                                    video_result2 = NOS_API.compare_pictures("sc_info_ref2", "sc_info", "[SC]")
                                                    video_result3 = NOS_API.compare_pictures("sc_info_ref3", "sc_info", "[SC]")
                                                    video_result4 = NOS_API.compare_pictures("sc_info_ref4", "sc_info", "[SC]")
                                                
                                                    ## Check is SC not detected
                                                    if (video_result1 >= NOS_API.thres or video_result2 >= NOS_API.thres or video_result3 >= NOS_API.thres or video_result4 >= NOS_API.thres):
                                                        
                                                        NOS_API.display_dialog("Reinsira o cart\xe3o e de seguida pressiona Continuar", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            
                                                        TEST_CREATION_API.send_ir_rc_command("[REDO_SC]")
                                                        
                                                        ## Perform grab picture
                                                        if not(NOS_API.grab_picture("sc_info")):
                                                            if (Repeat == 0):
                                                                Repeat = Repeat + 1
                                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                                else:
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3897.")
                                                                continue
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                                NOS_API.set_error_message("Reboot")
                                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                                
                                                                NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                
                                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                            
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                                        
                                                                NOS_API.send_report_over_mqtt_test_plan(
                                                                        test_result,
                                                                        end_time,
                                                                        error_codes,
                                                                        report_file)
                                                                        
                                                                ## Update test result
                                                                TEST_CREATION_API.update_test_result(test_result)
                                                                
                                                                ## Return DUT to initial state and de-initialize grabber device
                                                                NOS_API.deinitialize()
                                                                
                                                                return                        
                                                        
                                                        comp_result = NOS_API.compare_pictures("sc_info_ref1", "sc_info", "[CAS_ID_Place]")
                                                        comp_result1 = NOS_API.compare_pictures("sc_info_ref2", "sc_info", "[CAS_ID_Place]")
                                                        comp_result2 = NOS_API.compare_pictures("sc_info_ref3", "sc_info", "[CAS_ID_Place]")
                                                        comp_result3 = NOS_API.compare_pictures("sc_info_ref4", "sc_info", "[CAS_ID_Place]")
                                                        Flag = 0
                                                        while (comp_result < NOS_API.thres and comp_result1 < NOS_API.thres and comp_result2 < NOS_API.thres and comp_result3 < NOS_API.thres):
                                                            TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_DOWN]")
                                                            
                                                            ## Perform grab picture
                                                            if not(NOS_API.grab_picture("sc_info")):
                                                                if (Repeat == 0):
                                                                    Repeat = Repeat + 1
                                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                                    else:
                                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 3839.")
                                                                    Flag = 1
                                                                    break
                                                                else:
                                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                                    NOS_API.set_error_message("Reboot")
                                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                                    
                                                                    NOS_API.add_test_case_result_to_file_report(
                                                                                test_result,
                                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                                error_codes,
                                                                                error_messages)
                                                    
                                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                                    report_file = NOS_API.create_test_case_log_file(
                                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                    end_time)
                                                                
                                                                    NOS_API.upload_file_report(report_file)
                                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                                            
                                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                                            test_result,
                                                                            end_time,
                                                                            error_codes,
                                                                            report_file)
                                                                            
                                                                    ## Update test result
                                                                    TEST_CREATION_API.update_test_result(test_result)
                                                                    
                                                                    ## Return DUT to initial state and de-initialize grabber device
                                                                    NOS_API.deinitialize()
                                                                    
                                                                    return
                                                                                        
                                                            comp_result = NOS_API.compare_pictures("sc_info_ref1", "sc_info", "[CAS_ID_Place]")
                                                            comp_result1 = NOS_API.compare_pictures("sc_info_ref2", "sc_info", "[CAS_ID_Place]")
                                                            comp_result2 = NOS_API.compare_pictures("sc_info_ref3", "sc_info", "[CAS_ID_Place]")
                                                            comp_result3 = NOS_API.compare_pictures("sc_info_ref4", "sc_info", "[CAS_ID_Place]")
                                                        
                                                        if (Flag == 1):
                                                            continue
                                                        video_result1 = NOS_API.compare_pictures("sc_info_ref1", "sc_info", "[SC]")
                                                        video_result2 = NOS_API.compare_pictures("sc_info_ref2", "sc_info", "[SC]")
                                                        video_result3 = NOS_API.compare_pictures("sc_info_ref3", "sc_info", "[SC]")
                                                        video_result4 = NOS_API.compare_pictures("sc_info_ref4", "sc_info", "[SC]")
                                                    
                                                        ## Check is SC not detected
                                                        if (video_result1 >= NOS_API.thres or video_result2 >= NOS_API.thres or video_result3 >= NOS_API.thres or video_result4 >= NOS_API.thres):
                                                    
                                                            TEST_CREATION_API.write_log_to_file("Smart card is not detected")
                                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.sc_not_detected_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.sc_not_detected_error_message)
                                                            NOS_API.set_error_message("SmartCard")
                                                            error_codes = NOS_API.test_cases_results_info.sc_not_detected_error_code
                                                            error_messages = NOS_API.test_cases_results_info.sc_not_detected_error_message 
                                                            Repeat = 2
                                                        else:
                                                    
                                                            ## Extract SC number and CAS ID from image
                                                            sc_number = TEST_CREATION_API.OCR_recognize_text("sc_info", "[SC_NUMBER]", "[OCR_FILTER]", "sc_number")
                                                            cas_id_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                                                            NOS_API.test_cases_results_info.cas_id_number = cas_id_number
                                                            NOS_API.test_cases_results_info.sc_number = sc_number
                                                            
                                                            ## Log SC number and CAS ID
                                                            TEST_CREATION_API.write_log_to_file("The extracted sc number is: " + sc_number)
                                                            TEST_CREATION_API.write_log_to_file("The extracted cas id number is: " + cas_id_number)
                                                        
                                                            NOS_API.update_test_slot_comment("SC number: " + NOS_API.test_cases_results_info.sc_number \
                                                                            + "; cas id number: " + NOS_API.test_cases_results_info.cas_id_number)
                                                            
                                                            cas_id_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
                                                    
                                                            ## Compare CAS ID number with the CAS ID number previously scanned by barcode scanner
                                                            if (NOS_API.ignore_zero_letter_o_during_comparation(cas_id_number, cas_id_using_barcode)):                                                                                                    
                                                                #test_result = "PASS"  
                                                                Serial_Number_TestCase = True
                                                                TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("CAS ID number and CAS ID number previuosly scanned by barcode scanner is not the same")
                                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_cas_id_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.wrong_cas_id_error_message \
                                                                                                        + "; OCR: " + str(cas_id_number))
                                                                NOS_API.set_error_message("CAS ID")
                                                                error_codes = NOS_API.test_cases_results_info.wrong_cas_id_error_code
                                                                error_messages = NOS_API.test_cases_results_info.wrong_cas_id_error_message
                                                                Repeat = 2
                                                                
                                                    else:
                                                    
                                                        ## Extract SC number and CAS ID from image
                                                        sc_number = TEST_CREATION_API.OCR_recognize_text("sc_info", "[SC_NUMBER]", "[OCR_FILTER]", "sc_number")
                                                        cas_id_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                                                        NOS_API.test_cases_results_info.cas_id_number = cas_id_number
                                                        NOS_API.test_cases_results_info.sc_number = sc_number
                                                        
                                                        ## Log SC number and CAS ID
                                                        TEST_CREATION_API.write_log_to_file("The extracted sc number is: " + sc_number)
                                                        TEST_CREATION_API.write_log_to_file("The extracted cas id number is: " + cas_id_number)
                                                    
                                                        NOS_API.update_test_slot_comment("SC number: " + NOS_API.test_cases_results_info.sc_number \
                                                                        + "; cas id number: " + NOS_API.test_cases_results_info.cas_id_number)
                                                        
                                                        cas_id_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
                                                
                                                        ## Compare CAS ID number with the CAS ID number previously scanned by barcode scanner
                                                        if (NOS_API.ignore_zero_letter_o_during_comparation(cas_id_number, cas_id_using_barcode)):                                                                                                    
                                                            #test_result = "PASS"
                                                            Serial_Number_TestCase = True
                                                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("CAS ID number and CAS ID number previuosly scanned by barcode scanner is not the same")
                                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_cas_id_error_code \
                                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.wrong_cas_id_error_message \
                                                                                                    + "; OCR: " + str(cas_id_number))
                                                            NOS_API.set_error_message("CAS ID")
                                                            error_codes = NOS_API.test_cases_results_info.wrong_cas_id_error_code
                                                            error_messages = NOS_API.test_cases_results_info.wrong_cas_id_error_message 
                                                            Repeat = 2
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Ethernet Fail. IP address is 0.0.0.0")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.eth2_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.eth2_nok_error_message)
                                                    NOS_API.set_error_message("Eth")
                                                    error_codes = NOS_API.test_cases_results_info.eth2_nok_error_code
                                                    error_messages = NOS_API.test_cases_results_info.eth2_nok_error_message
                                                    Repeat = 2
                                                    #TEST_CREATION_API.write_log_to_file("IP address is 0.0.0.0")
                                                    #NOS_API.set_error_message("IP")
                                                    #error_codes = NOS_API.test_cases_results_info.ip_error_code
                                                    #error_messages = NOS_API.test_cases_results_info.ip_error_message
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Fail SNR")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_fail_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.snr_fail_error_message)
                                                NOS_API.set_error_message("SNR")
                                                error_codes = NOS_API.test_cases_results_info.snr_fail_error_code
                                                error_messages = NOS_API.test_cases_results_info.snr_fail_error_message 
                                                Repeat = 2
                                        else:
                                            TEST_CREATION_API.write_log_to_file("RX value is less than threshold")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.rx_fail_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.rx_fail_error_message)
                                            NOS_API.set_error_message("CM Docsis")
                                            error_codes = NOS_API.test_cases_results_info.rx_fail_error_code
                                            error_messages = NOS_API.test_cases_results_info.rx_fail_error_message
                                            Repeat = 2
                                    else:
                                        TEST_CREATION_API.write_log_to_file("TX value is less than threshold")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.tx_fail_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.tx_fail_error_message)
                                        NOS_API.set_error_message("CM Docsis")
                                        error_codes = NOS_API.test_cases_results_info.tx_fail_error_code
                                        error_messages = NOS_API.test_cases_results_info.tx_fail_error_message 
                                        Repeat = 2
                                else:
                                    TEST_CREATION_API.write_log_to_file("MAC number is not the same as previous scanned mac number")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_mac_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.wrong_mac_error_message)
                                    NOS_API.set_error_message("MAC")
                                    error_codes = NOS_API.test_cases_results_info.wrong_mac_error_code
                                    error_messages = NOS_API.test_cases_results_info.wrong_mac_error_message 
                                    Repeat = 2
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message  
                                Repeat = 2
                        else:
                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                            NOS_API.set_error_message("Reboot")
                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                            Repeat = 2
                        
                    else:
                        #NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                        NOS_API.set_error_message("Reboot")
                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                        Repeat = 2
                
            ##############################################################################################################################################################################################################################    
            #############################################################################################Interfaces#######################################################################################################################    
            ##############################################################################################################################################################################################################################
                        
                if (Serial_Number_TestCase):
                    TEST_CREATION_API.write_log_to_file("####Interfaces####")
                    NOS_API.give_me_give_me_give_me_a_time_after_finish("Verificação de Outros Parametros")   
                    
                    ## Max record audio time in miliseconds
                    MAX_RECORD_AUDIO_TIME = 2000
            
                    MAX_RECORD_VIDEO_TIME = 2000
            
                    THRESHOLD = 70
                    
                    ## Set test result default to FAIL
                    test_result = "FAIL"
                    test_result_hd = False
                    HD_SD_Result = False
                    error_codes = ""
                    error_messages = ""
                    
                    pqm_analyse_check = True
        
                    hd_counter = 0
                    sd_ch_counter = 0
                    
                    HDMI_VIDEO_Result = False        
                    test_result_COAX_output = False
                    SPDIF_Result = False      
                    test_result_SCART_video = False     
                    error_command_telnet = False
                    stb_state = False    
                    test_result_res = False  
                    test_result_SCART_audio = False
                    Telnet_Test_Result = False
                    test_result_ButtonLeds = False
                    HDMI_Result = False
                    VIDEO_RECORD_Result = False
                    AUDIO_RECORD_Result = False
        
                    
                    ## Set volume to max
                    TEST_CREATION_API.send_ir_rc_command("[VOL_MIN]")
                    
                    ## Set volume to half, because if vol is max, signal goes in saturation
                    TEST_CREATION_API.send_ir_rc_command("[VOL_PLUS_HALF]")
                    
                    ## Start grabber device with audio on default video source
                    TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
                    time.sleep(1)
        
                ######################################################################## HDMI Video 720p Test #################################################################################   
                
                    if not(NOS_API.is_signal_present_on_video_source()):
                        time.sleep(5)
                    time.sleep(1)
                    if (NOS_API.is_signal_present_on_video_source()):
                        
                        TEST_CREATION_API.send_ir_rc_command("[RESOLUTION_SETTINGS]")
                        if not (NOS_API.grab_picture("Resolution_Right_Place")):
                            if (Repeat == 0):
                                Repeat = Repeat + 1
                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1315.")
                                break
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                        
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                            
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                return
                        comparassion_result = NOS_API.compare_pictures("Resolution_Right_Place_1080_ref", "Resolution_Right_Place", "[Resolution_Right_Place_1080]")
                        comparassion_result_1 = NOS_API.compare_pictures("Resolution_Right_Place_1080_Black_ref", "Resolution_Right_Place", "[Resolution_Right_Place_1080]")
                        comparassion_result_2 = NOS_API.compare_pictures("Resolution_Right_Place_1080_ref2", "Resolution_Right_Place", "[Resolution_Right_Place_1080]")
                        comparassion_result_3 = NOS_API.compare_pictures("Resolution_Right_Place_1080_ref3", "Resolution_Right_Place", "[Resolution_Right_Place_1080]")
                        if not(comparassion_result >= 60 or comparassion_result_1 >= 80 or comparassion_result_2 >= 80 or comparassion_result_3 >= 80):
                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                            time.sleep(5)
                            TEST_CREATION_API.send_ir_rc_command("[RESOLUTION_SETTINGS_SLOW]")
                            if not (NOS_API.grab_picture("Resolution_Right_Place_1")):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 1315.")
                                    break
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                            
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                            comparassion_result = NOS_API.compare_pictures("Resolution_Right_Place_1080_ref", "Resolution_Right_Place_1", "[Resolution_Right_Place_720]")
                            comparassion_result_1 = NOS_API.compare_pictures("Resolution_Right_Place_1080_Black_ref", "Resolution_Right_Place", "[Resolution_Right_Place_1080]")
                            comparassion_result_2 = NOS_API.compare_pictures("Resolution_Right_Place_1080_ref2", "Resolution_Right_Place", "[Resolution_Right_Place_1080]")
                            comparassion_result_3 = NOS_API.compare_pictures("Resolution_Right_Place_1080_ref3", "Resolution_Right_Place", "[Resolution_Right_Place_1080]")
                            if not(comparassion_result >= 60 or comparassion_result_1 >= 80 or comparassion_result_2 >= 80 or comparassion_result_3 >= 80):
                                NOS_API.set_error_message("Navegação")
                                TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - " + str(modulation) + " " + str(frequencia) + " -",
                                                            ">50<70 <1.0E-6 - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)                           
                                            
                                return
                        
                        TEST_CREATION_API.send_ir_rc_command("[Change_Resolution_HD]")
                        time.sleep(3)
                        
                        if not(NOS_API.is_signal_present_on_video_source()):
                            time.sleep(2)
                        if (NOS_API.is_signal_present_on_video_source()):
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "720"):
                                try:
                                    NOS_API.grab_picture("Debug")
                                except:
                                    pass
                                TEST_CREATION_API.write_log_to_file("Resolution: " + video_height)
                                NOS_API.set_error_message("Resolução")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                Repeat = 2
                            else:
                                test_result_res = True
                        else:
                            if (Repeat == 0):
                                Repeat = Repeat + 1
                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4173.")
                                continue
                            else:
                                #NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                TEST_CREATION_API.write_log_to_file("STB lost Signal after change Resolution.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                Repeat = 2
                                
                        
                        
                        #TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_new]")
                        #time.sleep(1)
                        #
                        #if not(NOS_API.is_signal_present_on_video_source()):
                        #    time.sleep(2)
                        #if (NOS_API.is_signal_present_on_video_source()):
                        #
                        #    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        #    if (video_height != "720"):
                        #        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p]")
                        #        time.sleep(5)
                        #
                        #        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        #        if (video_height != "720"):
                        #            NOS_API.set_error_message("Resolução")
                        #            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                        #                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                        #            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                        #            error_messages = NOS_API.test_cases_results_info.resolution_error_message
                        #            Repeat = 2
                        #        else:
                        #            test_result_res = True
                        #    else:
                        #        test_result_res = True
                        #else:
                        #    if (Repeat == 0):
                        #        Repeat = Repeat + 1
                        #        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4173.")
                        #        continue
                        #    else:
                        #        NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                        #        TEST_CREATION_API.write_log_to_file("STB lost Signal after change Resolution.Possible Reboot.")
                        #        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                        #                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                        #        NOS_API.set_error_message("Reboot")
                        #        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                        #        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                        #        Repeat = 2
                    else:
                        #NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                        NOS_API.set_error_message("Reboot")
                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                        error_messages = NOS_API.test_cases_results_info.reboot_error_message  
                        Repeat = 2
                    
                    if (test_result_res):
                        NOS_API.give_me_give_me_give_me_a_time_after_finish("Colocar volume a meio / Mudar Resolução") 
                        
                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                        time.sleep(2)
                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                        time.sleep(1)
                        
                        if not (NOS_API.is_signal_present_on_video_source()):
                            if (Repeat == 0):
                                Repeat = Repeat + 1
                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4205.")
                                continue
                            else:
                                #NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                NOS_API.deinitialize()
                                NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                            
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                                NOS_API.upload_file_report(report_file)
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                                
                                return
                            
                        TEST_CREATION_API.send_ir_rc_command("[Check_Record_Active]")
                                    
                        if not(NOS_API.grab_picture("Active_Recording")):
                            if (Repeat == 0):
                                Repeat = Repeat + 1
                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4246.")
                                continue
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                            
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                return
                                
                        comparassion_result = NOS_API.compare_pictures("Recording_Active_ref", "Active_Recording", "[Menu_Arquivo]")
                        comparassion_scn_result = NOS_API.compare_pictures("Recording_Active_new_ref", "Active_Recording", "[Menu_Arquivo]")
                        
                        if(comparassion_result < NOS_API.thres and comparassion_scn_result < NOS_API.thres): 
                            if not(NOS_API.grab_picture("Active_Recording_First")):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4294.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                    
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                            #if not(NOS_API.wait_for_picture(["Recording_Active_ref"], 30, "[Menu_Arquivo]", 0.0)):
                            compare_result = NOS_API.wait_for_multiple_pictures(["Recording_Active_ref", "Recording_Active_new_ref"], 30, ["[Menu_Arquivo]", "[Menu_Arquivo]"], [NOS_API.thres, NOS_API.thres])
                            if (compare_result == -1 or compare_result == -2):
                                TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command("[Check_Record_Active]")
                                #if not(NOS_API.wait_for_picture(["Recording_Active_ref"], 30, "[Menu_Arquivo]", 0.0)):
                                compare_result = NOS_API.wait_for_multiple_pictures(["Recording_Active_ref", "Recording_Active_new_ref"], 30, ["[Menu_Arquivo]", "[Menu_Arquivo]"], [NOS_API.thres, NOS_API.thres])
                                if (compare_result == -1 or compare_result == -2):
                                    if not(NOS_API.grab_picture("Active_Recording_Second")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4343.")
                                            continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    TEST_CREATION_API.write_log_to_file("Navigation to HDD Menu failed")
                                    NOS_API.set_error_message("Navegação")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                    error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                    error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
        
        
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
        
                                    return
                            if not(NOS_API.grab_picture("Active_Recording")):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4426.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                    
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                        video_result = NOS_API.compare_pictures("Recording_Active_ref", "Active_Recording", "[Active_Record]")
                        
                        if(video_result > NOS_API.thres):
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                            if not(NOS_API.grab_picture("Active_Recording_Playing")):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4474.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                    
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                            video_result_1 = NOS_API.compare_pictures("Record_Playing_ref", "Active_Recording_Playing", "[Check_Playing]")
                            if(video_result_1 > NOS_API.thres):
                                TEST_CREATION_API.send_ir_rc_command("[Stop_Playing]")
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                            if not(NOS_API.grab_picture("Check_Keep_Watching")):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4523.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                    
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                            video_result_2 = NOS_API.compare_pictures("Record_Kepp_Watching_ref", "Check_Keep_Watching", "[Keep_Watching_Check]")
                            if(video_result_2 > NOS_API.thres):
                                TEST_CREATION_API.send_ir_rc_command("[Erase_Active_Record]")
                                time.sleep(1.5)
                            else:
                                TEST_CREATION_API.send_ir_rc_command("[Erase_Active_Record_2]")
                                time.sleep(1.5)
                            
                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                        time.sleep(5)
                        
                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                        time.sleep(2)
                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                        time.sleep(1)
                        
                        TEST_CREATION_API.send_ir_rc_command("[REC]")
                        
                        time.sleep(0.8)

                        if not(NOS_API.grab_picture("REC")):
                            if (Repeat == 0):
                                Repeat = Repeat + 1
                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                else:
                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4587.")
                                continue
                            else:
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                test_result = "FAIL"
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                        
                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                    
                            
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return

                        video_result1 = NOS_API.compare_pictures("Rec_ref", "REC", "[REC]")
                        video_result2 = NOS_API.compare_pictures("Rec1_ref", "REC", "[REC]")
                        video_result3 = NOS_API.compare_pictures("Rec2_ref", "REC", "[REC]")
        
                        if not(video_result1 >= 60 or video_result2 >= 60 or video_result3 >= 60):
                            if not(NOS_API.grab_picture("Check_Full_HDD")):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4638.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                    
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                            video_result3 = NOS_API.compare_pictures("Check_Full_HDD_ref", "Check_Full_HDD", "[Check_Full_HDD]")
                            video_result4 = NOS_API.compare_pictures("Check_Full_HDD2_ref", "Check_Full_HDD", "[Check_Full_HDD]")
                            
                            if (video_result3 >= 60 or video_result4 >= 60):
                                TEST_CREATION_API.send_ir_rc_command("[Erase_HDD]")
                                if not(NOS_API.grab_picture("Check_Serie_Priority")):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4687.")
                                        continue
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return
                                
                                check_result = NOS_API.compare_pictures("Check_Serie_Priority_ref", "Check_Serie_Priority", "[Serie_Priority]")
                                check_result_1 = NOS_API.compare_pictures("Check_Serie_Priority_Sched_ref", "Check_Serie_Priority", "[Serie_Priority]")
                                if (check_result >= NOS_API.thres):
                                    TEST_CREATION_API.send_ir_rc_command("[Serie_Priority]")
                                else:
                                    if(check_result_1 >= NOS_API.thres):
                                        TEST_CREATION_API.send_ir_rc_command("[Serie_Priority_new]")
                                    else:
                                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                                    
                                if not(NOS_API.grab_picture("Check_Right_Menu")):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4742.")
                                        continue
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return
                                
                                video_result = NOS_API.compare_pictures("Erase_Right_Menu_ref", "Check_Right_Menu", "[Erase_Right_Menu]")
                                video_result_1 = NOS_API.compare_pictures("Erase_Right_Menu2_ref", "Check_Right_Menu", "[Erase_Right_Menu_new]")
                                
                                if not(video_result >= NOS_API.thres or video_result_1 >= NOS_API.thres):
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[Erase_HDD]")
                                    
                                    if not(NOS_API.grab_picture("Check_Serie_Priority_1")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4795.")
                                            continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    
                                    check_result = NOS_API.compare_pictures("Check_Serie_Priority_ref", "Check_Serie_Priority_1", "[Serie_Priority]")
                                    check_result_1 = NOS_API.compare_pictures("Check_Serie_Priority_Sched_ref", "Check_Serie_Priority_1", "[Serie_Priority]")
                                    if (check_result >= NOS_API.thres):
                                        TEST_CREATION_API.send_ir_rc_command("[Serie_Priority]")
                                    else:
                                        if(check_result_1 >= NOS_API.thres):
                                            TEST_CREATION_API.send_ir_rc_command("[Serie_Priority_new]")
                                        else:
                                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                                        
                                    if not(NOS_API.grab_picture("Check_Right_Menu_1")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4846.")
                                            continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    
                                    video_result = NOS_API.compare_pictures("Erase_Right_Menu_ref", "Check_Right_Menu_1", "[Erase_Right_Menu]")
                                    video_result_1 = NOS_API.compare_pictures("Erase_Right_Menu2_ref", "Check_Right_Menu_1", "[Erase_Right_Menu_new]")
                                
                                    if not(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                        TEST_CREATION_API.write_log_to_file("Couldn't navigate to HDD Menu")
                                        NOS_API.set_error_message("Navegação")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                        error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""    
                                        
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        return
                            
                                TEST_CREATION_API.send_ir_rc_command("[Erase_HDD2]")
                                
                                result = NOS_API.wait_for_multiple_pictures(["Erase_Success_ref"],90,["[Erase_Success]"],[NOS_API.thres])
                                
                                if (result == -2):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 4937.")
                                        continue
                                    else:
                                        test_result = "FAIL"
                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                    
                        
                                        return
                                elif(result == 0):
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                    time.sleep(2)
                                else:
                                    TEST_CREATION_API.write_log_to_file("Doesn't Erase HDD")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdd_erase_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdd_erase_error_message)
                                    error_codes = NOS_API.test_cases_results_info.hdd_erase_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdd_erase_error_message
                                    NOS_API.set_error_message("HDD")
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = ""    
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                    
                                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    return
                                
                            TEST_CREATION_API.send_ir_rc_command("[REC]")
                            time.sleep(0.8)
                            if not(NOS_API.grab_picture("REC_1")):
                                if (Repeat == 0):
                                    Repeat = Repeat + 1
                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                    else:
                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5027.")
                                    continue
                                else:
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                    NOS_API.set_error_message("Reboot")
                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                    
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                    end_time)
                                
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                                            
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                            
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    return
                            
                            video_result1 = NOS_API.compare_pictures("Rec_ref", "REC_1", "[REC]")
                            video_result2 = NOS_API.compare_pictures("Rec1_ref", "REC_1", "[REC]")
                            video_result3 = NOS_API.compare_pictures("Rec2_ref", "REC_1", "[REC]")
                        
                            if not(video_result1 >= 70 or video_result2 >= 70 or video_result3 >= 70):
                                if not(NOS_API.grab_picture("Check_Full_HDD")):
                                    if (Repeat == 0):
                                        Repeat = Repeat + 1
                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                        else:
                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5076.")
                                        continue
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                        NOS_API.set_error_message("Reboot")
                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                        
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                        end_time)
                                    
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                                
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        return
                                video_result3 = NOS_API.compare_pictures("Check_Full_HDD_ref", "Check_Full_HDD", "[Check_Full_HDD]")
                                video_result4 = NOS_API.compare_pictures("Check_Full_HDD2_ref", "Check_Full_HDD", "[Check_Full_HDD]")
                                
                                if (video_result3 >= 60 or video_result4 >= 60):
                                    TEST_CREATION_API.send_ir_rc_command("[Erase_HDD]")
                                    if not(NOS_API.grab_picture("Check_Serie_Priority")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5125.")
                                            continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    
                                    check_result = NOS_API.compare_pictures("Check_Serie_Priority_ref", "Check_Serie_Priority", "[Serie_Priority]")
                                    check_result_1 = NOS_API.compare_pictures("Check_Serie_Priority_Sched_ref", "Check_Serie_Priority", "[Serie_Priority]")
                                    if (check_result >= NOS_API.thres):
                                        TEST_CREATION_API.send_ir_rc_command("[Serie_Priority]")
                                    else:
                                        if(check_result_1 >= NOS_API.thres):
                                            TEST_CREATION_API.send_ir_rc_command("[Serie_Priority_new]")
                                        else:
                                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                                        
                                    if not(NOS_API.grab_picture("Check_Right_Menu")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5176.")
                                            continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    
                                    video_result = NOS_API.compare_pictures("Erase_Right_Menu_ref", "Check_Right_Menu", "[Erase_Right_Menu]")
                                    video_result_1 = NOS_API.compare_pictures("Erase_Right_Menu2_ref", "Check_Right_Menu", "[Erase_Right_Menu_new]")
                                
                                    if not(video_result >= NOS_API.thres or video_result_1 >= NOS_API.thres):
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                        time.sleep(2)
                                        TEST_CREATION_API.send_ir_rc_command("[Erase_HDD]")
                                        
                                        if not(NOS_API.grab_picture("Check_Serie_Priority_1")):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5229.")
                                                continue
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return
                                        
                                        check_result = NOS_API.compare_pictures("Check_Serie_Priority_ref", "Check_Serie_Priority_1", "[Serie_Priority]")
                                        check_result_1 = NOS_API.compare_pictures("Check_Serie_Priority_Sched_ref", "Check_Serie_Priority_1", "[Serie_Priority]")
                                        if (check_result >= NOS_API.thres):
                                            TEST_CREATION_API.send_ir_rc_command("[Serie_Priority]")
                                        else:
                                            if(check_result_1 >= NOS_API.thres):
                                                TEST_CREATION_API.send_ir_rc_command("[Serie_Priority_new]")
                                            else:
                                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                            
                                        if not(NOS_API.grab_picture("Check_Right_Menu_1")):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5280.")
                                                continue
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return
                                        
                                        video_result = NOS_API.compare_pictures("Erase_Right_Menu_ref", "Check_Right_Menu_1", "[Erase_Right_Menu]")
                                        video_result_1 = NOS_API.compare_pictures("Erase_Right_Menu2_ref", "Check_Right_Menu_1", "[Erase_Right_Menu_new]")
                                
                                        if not(video_result >= NOS_API.thres or video_result_1 >= NOS_API.thres):
                                            TEST_CREATION_API.write_log_to_file("Couldn't navigate to HDD Menu")
                                            NOS_API.set_error_message("Navegação")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                            error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = ""    
                                            
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
        
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            return
                                
                                    TEST_CREATION_API.send_ir_rc_command("[Erase_HDD2]")
                                    
                                    result = NOS_API.wait_for_multiple_pictures(["Erase_Success_ref"],90,["[Erase_Success]"],[NOS_API.thres])
                                    
                                    if (result == -2):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5371.")
                                            continue
                                        else:
                                            test_result = "FAIL"
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    elif(result == 0):
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                        time.sleep(2)
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Doesn't Erase HDD")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdd_erase_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdd_erase_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdd_erase_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdd_erase_error_message
                                        NOS_API.set_error_message("HDD")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""    
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                    
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        return
                                    
                                    TEST_CREATION_API.send_ir_rc_command("[REC]")
                                    time.sleep(0.8)
                                    if not(NOS_API.grab_picture("REC_1")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5462.")
                                            continue
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    
                                    video_result1 = NOS_API.compare_pictures("Rec_ref", "REC_1", "[REC]")
                                    video_result2 = NOS_API.compare_pictures("Rec1_ref", "REC_1", "[REC]")
                                    video_result3 = NOS_API.compare_pictures("Rec2_ref", "REC_1", "[REC]")
                                
                                    if not(video_result1 >= 70 or video_result2 >= 70 or video_result3 >= 70):
                                        if not(NOS_API.display_custom_dialog("O Led REC est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                            NOS_API.test_cases_results_info.recording_started = False
                                            TEST_CREATION_API.write_log_to_file("Recording is not started")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recording_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.recording_error_message)
                                            error_codes = NOS_API.test_cases_results_info.recording_error_code
                                            error_messages = NOS_API.test_cases_results_info.recording_error_message
                                            NOS_API.set_error_message("HDD")
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
        
        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
        
                                            return
                                    
                                else:
                                    if not(NOS_API.display_custom_dialog("O Led REC est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                        NOS_API.test_cases_results_info.recording_started = False
                                        TEST_CREATION_API.write_log_to_file("Recording is not started")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recording_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.recording_error_message)
                                        error_codes = NOS_API.test_cases_results_info.recording_error_code
                                        error_messages = NOS_API.test_cases_results_info.recording_error_message
                                        NOS_API.set_error_message("HDD")
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
        
        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
        
                                        return
                                
                                
                        time.sleep(1)
                        
                        NOS_API.give_me_give_me_give_me_a_time_after_finish("Verificar se tem Gravações ativas / Iniciar Gravação") 
                        
                        ## Record video with duration of recording (10 seconds)
                        NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                
                        ## Instance of PQMAnalyse type
                        pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                
                        ## Set what algorithms should be checked while analyzing given video file with PQM.
                        # Attributes are set to false by default.
                        pqm_analyse.black_screen_activ = True
                        pqm_analyse.blocking_activ = True
                        pqm_analyse.freezing_activ = True
                
                        # Name of the video file that will be analysed by PQM.
                        pqm_analyse.file_name = "video"
                
                        ## Analyse recorded video
                        analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                
                        if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message)
                                    
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message
                
                        if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                                    
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                            
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                        
                        if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                                    
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                        
                        if not(pqm_analyse_check):  
                            NOS_API.set_error_message("Video HDMI")
                            NOS_API.deinitialize()
                            NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                        
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                            NOS_API.upload_file_report(report_file)
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                            
                            return
                        
                        if not(analysed_video):
                            TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                            error_codes = NOS_API.test_cases_results_info.grabber_error_code
                            error_messages = NOS_API.test_cases_results_info.grabber_error_message
                            NOS_API.set_error_message("Inspection")
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                    
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return                       
                                
                        ## Check if video is playing (check if video is not freezed)
                        if not(NOS_API.is_video_playing()):
                            time.sleep(5)
                            if not(NOS_API.is_video_playing()):
                                Is_Playing = False
                            else:
                                Is_Playing = True
                        else:
                            Is_Playing = True
                        if(Is_Playing):
                    
                            video_result1 = 0
                            video_result2 = 0
                            video_result3 = 0
                            
                            i = 0
                            
                            while(i < 3):
                    
                                try:
                                    ## Perform grab picture
                                    if not(NOS_API.grab_picture("HDMI_video")):
                                        if (Repeat == 0):
                                            Repeat = Repeat + 1
                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                            else:
                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5371.")
                                            Break_Cicle = True
                                            break
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                            NOS_API.set_error_message("Reboot")
                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return
                                    ## Compare grabbed and expected image and get result of comparison
                                    video_result1 = NOS_API.compare_pictures("HDMI_video_ref1", "HDMI_video", "[HALF_SCREEN]")
                                    video_result2 = NOS_API.compare_pictures("HDMI_video_ref2", "HDMI_video", "[HALF_SCREEN]")
                                    video_result3 = NOS_API.compare_pictures("HDMI_video_ref3", "HDMI_video", "[HALF_SCREEN]")
                                    video_result4 = NOS_API.compare_pictures("HDMI_video_ref4", "HDMI_video", "[HALF_SCREEN]")
                                    video_result5 = NOS_API.compare_pictures("HDMI_video_ref5", "HDMI_video", "[HALF_SCREEN]")
                            
                                except:
                                    i = i + 1
                                    continue
                                
                                ## Check video analysis results and update comments
                                if (video_result1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or \
                                    video_result3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result4 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or \
                                    video_result5 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    i = 0
                                    if (analysed_video):            
                                        HDMI_VIDEO_Result = True
                                    else:
                                        NOS_API.set_error_message("Video HDMI") 
                                    break
                                i = i + 1
                            
                            if(Break_Cicle):
                                continue
                                
                            if (i >= 3): 
                                TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on HDMI 720p.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_576p_noise_error_message
                                NOS_API.set_error_message("Video HDMI") 
                                Repeat = 2  
                        else:
                            TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on HDMI 720p.")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                            NOS_API.set_error_message("Video HDMI") 
                            Repeat = 2
                        
                        if(HDMI_VIDEO_Result):
                            TEST_CREATION_API.record_audio("HDMI_audio_720", MAX_RECORD_AUDIO_TIME)
                            
                            audio_result_1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_720")
        
                            if not(audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD):                       
                                TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                time.sleep(5)
                                ## Record audio from digital output (HDMI)
                                TEST_CREATION_API.record_audio("HDMI_audio_720_1", MAX_RECORD_AUDIO_TIME)
                    
                                ## Compare recorded and expected audio and get result of comparison
                                audio_result_1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_720_1")
                               
                            if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                HDMI_Result = True                                                       
                            else:
                                #try:
                                #    ## Return DUT to initial state and de-initialize grabber device
                                #    NOS_API.deinitialize()
                                #except: 
                                #    pass
                                #    
                                #NOS_API.Inspection = True
                                #
                                #if (NOS_API.configure_power_switch_by_inspection()):
                                #    if not(NOS_API.power_off()): 
                                #        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                #        ## Update test result
                                #        TEST_CREATION_API.update_test_result(test_result)
                                #        NOS_API.set_error_message("Inspection")
                                #        
                                #        NOS_API.add_test_case_result_to_file_report(
                                #                        test_result,
                                #                        "- - - - - - - - - - - - - - - - - - - -",
                                #                        "- - - - - - - - - - - - - - - - - - - -",
                                #                        error_codes,
                                #                        error_messages)
                                #        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                #        report_file = ""
                                #        if (test_result != "PASS"):
                                #            report_file = NOS_API.create_test_case_log_file(
                                #                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                #                            NOS_API.test_cases_results_info.nos_sap_number,
                                #                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                #                            "",
                                #                            end_time)
                                #            NOS_API.upload_file_report(report_file)
                                #            NOS_API.test_cases_results_info.isTestOK = False
                                #        
                                #        
                                #        ## Update test result
                                #        TEST_CREATION_API.update_test_result(test_result)
                                #    
                                #        ## Return DUT to initial state and de-initialize grabber device
                                #        NOS_API.deinitialize()
                                #        
                                #        NOS_API.send_report_over_mqtt_test_plan(
                                #                    test_result,
                                #                    end_time,
                                #                    error_codes,
                                #                    report_file)
                                #
                                #        return
                                #    time.sleep(10)
                                #    ## Power on STB with energenie
                                #    if not(NOS_API.power_on()):
                                #        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                #        ## Update test result
                                #        TEST_CREATION_API.update_test_result(test_result)
                                #        NOS_API.set_error_message("Inspection")
                                #        
                                #        NOS_API.add_test_case_result_to_file_report(
                                #                        test_result,
                                #                        "- - - - - - - - - - - - - - - - - - - -",
                                #                        "- - - - - - - - - - - - - - - - - - - -",
                                #                        error_codes,
                                #                        error_messages)
                                #        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                #        report_file = ""
                                #        if (test_result != "PASS"):
                                #            report_file = NOS_API.create_test_case_log_file(
                                #                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                #                            NOS_API.test_cases_results_info.nos_sap_number,
                                #                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                #                            "",
                                #                            end_time)
                                #            NOS_API.upload_file_report(report_file)
                                #            NOS_API.test_cases_results_info.isTestOK = False
                                #        
                                #        test_result = "FAIL"
                                #        
                                #        ## Update test result
                                #        TEST_CREATION_API.update_test_result(test_result)
                                #    
                                #        ## Return DUT to initial state and de-initialize grabber device
                                #        NOS_API.deinitialize()
                                #        
                                #        NOS_API.send_report_over_mqtt_test_plan(
                                #                test_result,
                                #                end_time,
                                #                error_codes,
                                #                report_file)
                                #        
                                #        return
                                #    time.sleep(15)
                                #else:
                                #    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                                #    
                                #    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                #                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                #    NOS_API.set_error_message("Inspection")
                                #    
                                #    NOS_API.add_test_case_result_to_file_report(
                                #                    test_result,
                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                #                    error_codes,
                                #                    error_messages)
                                #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                #    report_file = ""
                                #    if (test_result != "PASS"):
                                #        report_file = NOS_API.create_test_case_log_file(
                                #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                #                        NOS_API.test_cases_results_info.nos_sap_number,
                                #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                #                        "",
                                #                        end_time)
                                #        NOS_API.upload_file_report(report_file)
                                #        NOS_API.test_cases_results_info.isTestOK = False
                                #    
                                #    test_result = "FAIL"
                                #    ## Update test result
                                #    TEST_CREATION_API.update_test_result(test_result)
                                #    
                                #
                                #    ## Return DUT to initial state and de-initialize grabber device
                                #    NOS_API.deinitialize()
                                #    
                                #    NOS_API.send_report_over_mqtt_test_plan(
                                #        test_result,
                                #        end_time,
                                #        error_codes,
                                #        report_file)
                                #    
                                #    return
                                #
                                #NOS_API.Inspection = False
                                #
                                #NOS_API.initialize_grabber()
                                #
                                ### Start grabber device with audio on default video source
                                #NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                #TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
                                #time.sleep(1)
                                #
                                ### Record audio from digital output (HDMI 720)
                                #TEST_CREATION_API.record_audio("HDMI_audio_720_2", MAX_RECORD_AUDIO_TIME)
                                #
                                #audio_result_1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_720_2")
                                #
                                #if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                #    HDMI_Result = True 
                                #else:
                                    #if (TEST_CREATION_API.is_audio_present("HDMI_audio_720_2")):
                                if (TEST_CREATION_API.is_audio_present("HDMI_audio_720_1")):
                                    TEST_CREATION_API.write_log_to_file("Audio Absence on HDMI.")
                                    NOS_API.set_error_message("Audio HDMI")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                    Repeat = 2
                                else:
                                    TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                    NOS_API.set_error_message("Audio HDMI")
                                    NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                            + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                    Repeat = 2
                    
                ######################################################################## SPDIF Test #################################################################################   
        
                    if(HDMI_Result):     
                        NOS_API.grabber_stop_audio_source()
                        time.sleep(1)
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
        
                        ## Start grabber device with audio on SPDIF Coaxial source
                        TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.SPDIF_COAX)
                        time.sleep(1)
        
                        ## Record audio from digital output (SPDIF COAX)
                        TEST_CREATION_API.record_audio("SPDIF_COAX_audio", MAX_RECORD_AUDIO_TIME)
                        
                        #############Comparacao com referencia audio NOK############################################
                        
                        ## Compare recorded and expected audio and get result of comparison
                        audio_result1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_COAX_audio")
        
                        if not(audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
        
                            ## Check is audio present on channel
                            if (TEST_CREATION_API.is_audio_present("SPDIF_COAX_audio")):
                                test_result_COAX_output = True
                            else:
                                TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF coaxial interface.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message)
                                error_codes = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code
                                error_messages = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message 
                                NOS_API.set_error_message("SPDIF")
                                Repeat = 2
                        else:
                            time.sleep(3)
                            
                            NOS_API.display_dialog("Confirme o cabo SPDIF e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            
                            ## Record audio from digital output (SPDIF COAX)
                            TEST_CREATION_API.record_audio("SPDIF_COAX_audio1", MAX_RECORD_AUDIO_TIME)
                        
                            ## Compare recorded and expected audio and get result of comparison
                            audio_result1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_COAX_audio1")
                        
                            if not(audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                        
                                ## Check is audio present on channel
                                if (TEST_CREATION_API.is_audio_present("SPDIF_COAX_audio1")):
                                    test_result_COAX_output = True
                                else:
                                    TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF coaxial interface.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message)
                                    error_codes = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message 
                                    NOS_API.set_error_message("SPDIF")
                                    Repeat = 2
                            else:  
                                try:
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                except: 
                                    pass
                                    
                                NOS_API.Inspection = True
                                
                                if (NOS_API.configure_power_switch_by_inspection()):
                                    if not(NOS_API.power_off()): 
                                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        NOS_API.set_error_message("Inspection")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            "",
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                    
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)

                                        return
                                    time.sleep(10)
                                    ## Power on STB with energenie
                                    if not(NOS_API.power_on()):
                                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        NOS_API.set_error_message("Inspection")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            "",
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        test_result = "FAIL"
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                    
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                        
                                        return
                                    time.sleep(15)
                                else:
                                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                                    
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                    NOS_API.set_error_message("Inspection")
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        "",
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    test_result = "FAIL"
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    return
                                
                                NOS_API.Inspection = False
                                
                                NOS_API.initialize_grabber()
                                
                                ## Start grabber device with audio on SPDIF Coaxial source
                                TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.SPDIF_COAX)
                                time.sleep(1)
                                
                                ## Record audio from digital output (SPDIF COAX)
                                TEST_CREATION_API.record_audio("SPDIF_COAX_audio2", MAX_RECORD_AUDIO_TIME)
                            
                                ## Compare recorded and expected audio and get result of comparison
                                audio_result1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_COAX_audio2")
                            
                                if not(audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            
                                    ## Check is audio present on channel
                                    if (TEST_CREATION_API.is_audio_present("SPDIF_COAX_audio2")):
                                        test_result_COAX_output = True
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF coaxial interface.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message)
                                        error_codes = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code
                                        error_messages = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message 
                                        NOS_API.set_error_message("SPDIF")
                                        Repeat = 2
                                else:  
                                    TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SPDIF coaxial interface.")
                                    NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_code  \
                                                                                + ";\n" + NOS_API.test_cases_results_info.spdif_coaxial_signal_interference_error_code  \
                                                                                + "; Error messages: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_message \
                                                                                + ";\n" + NOS_API.test_cases_results_info.spdif_coaxial_signal_interference_error_message)
                                    error_codes = NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.spdif_coaxial_signal_interference_error_code
                                    error_messages = NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_message + " " +  NOS_API.test_cases_results_info.spdif_coaxial_signal_interference_error_message
                                    NOS_API.set_error_message("SPDIF")
                                    Repeat = 2
                        
                        if(test_result_COAX_output):
                        
                            NOS_API.grabber_stop_audio_source()
                            time.sleep(0.5)
                        
                            ## Start grabber device with audio on default audio source
                            TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.SPDIF_OPT)
                            time.sleep(2)        
                        
                            ## Record audio from digital output (SPDIF OPT)
                            TEST_CREATION_API.record_audio("SPDIF_OPT_audio", MAX_RECORD_AUDIO_TIME)

                            #############Comparacao com referencia audio NOK############################################
                            
                            ## Compare recorded and expected audio and get result of comparison
                            audio_result_1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_OPT_audio")
                        
                            if (audio_result_1 > TEST_CREATION_API.AUDIO_THRESHOLD):
                                                        
                                TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                time.sleep(3)
                                TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                time.sleep(3)
                                TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                ## Record audio from digital output (HDMI)
                                TEST_CREATION_API.record_audio("SPDIF_OPT_audio", MAX_RECORD_AUDIO_TIME)
                            
                                ## Compare recorded and expected audio and get result of comparison
                                audio_result_1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_OPT_audio")       
                        
                            if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                        
                                ## Check is audio present on channel
                                if (TEST_CREATION_API.is_audio_present("SPDIF_OPT_audio")):
                                    SPDIF_Result = True
                                
                                else:
                                    TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF optical interface.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message)
                                    error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message
                                    NOS_API.set_error_message("TOSLINK")
                                    Repeat = 2
                            else:
                                time.sleep(3)
                                
                                NOS_API.display_dialog("Confirme o cabo TOSLINK e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                
                                ## Record audio from digital output (SPDIF OPT)
                                TEST_CREATION_API.record_audio("SPDIF_OPT_audio_1", MAX_RECORD_AUDIO_TIME)
                                
                                ## Compare recorded and expected audio and get result of comparison
                                audio_result_1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_OPT_audio_1")
                                
                                if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                
                                    ## Check is audio present on channel
                                    if (TEST_CREATION_API.is_audio_present("SPDIF_OPT_audio_1")):
                                        SPDIF_Result = True
                                        
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF optical interface.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message)
                                        error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code
                                        error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message
                                        NOS_API.set_error_message("TOSLINK")
                                        Repeat = 2
                                else: 
                                    try:
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                    except: 
                                        pass
                                        
                                    NOS_API.Inspection = True
                                    
                                    if (NOS_API.configure_power_switch_by_inspection()):
                                        if not(NOS_API.power_off()): 
                                            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            NOS_API.set_error_message("Inspection")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                "",
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                        
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)

                                            return
                                        time.sleep(10)
                                        ## Power on STB with energenie
                                        if not(NOS_API.power_on()):
                                            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            NOS_API.set_error_message("Inspection")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                "",
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            test_result = "FAIL"
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                        
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                            
                                            return
                                        time.sleep(15)
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                                        
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                        NOS_API.set_error_message("Inspection")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            "",
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        test_result = "FAIL"
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                    
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                        
                                        return
                                    
                                    NOS_API.Inspection = False
                                    
                                    NOS_API.initialize_grabber()
                                    
                                    ## Start grabber device with audio on default audio source
                                    TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.SPDIF_OPT)
                                    time.sleep(2)  
                                    
                                    ## Record audio from digital output (SPDIF OPT)
                                    TEST_CREATION_API.record_audio("SPDIF_OPT_audio_2", MAX_RECORD_AUDIO_TIME)
                                    
                                    ## Compare recorded and expected audio and get result of comparison
                                    audio_result_1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_OPT_audio_2")
                                    
                                    if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    
                                        ## Check is audio present on channel
                                        if (TEST_CREATION_API.is_audio_present("SPDIF_OPT_audio_2")):
                                            SPDIF_Result = True
                                            
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF optical interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message)
                                            error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_absence_error_message
                                            NOS_API.set_error_message("TOSLINK")
                                            Repeat = 2
                                    else: 
                                        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SPDIF optical interface.")
                                        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_code  \
                                                                                    + ";\n" + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_code  \
                                                                                    + "; Error messages: " + NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_message \
                                                                                    + ";\n" + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_message)
                                        error_codes = NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_code
                                        error_messages = NOS_API.test_cases_results_info.spdif_optical_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.spdif_optical_signal_interference_error_message
                                        NOS_API.set_error_message("TOSLINK")
                                        Repeat = 2
                
        
                ######################################################################## SCART Test #################################################################################   
        
                        if(SPDIF_Result):   
        
                            NOS_API.grabber_stop_audio_source()
                            time.sleep(1)                            
        
                            ## Initialize input interfaces of DUT RT-AV101 device  
                            NOS_API.reset_dut()
        
                            ## Start grabber device with video on default video source
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                            
                            if not(NOS_API.is_signal_present_on_video_source()):
                                NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            
                            if (NOS_API.is_signal_present_on_video_source()):
        
                                ## Check if video is playing (check if video is not freezed)
                                if not(NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.CVBS2)):
                                    time.sleep(5)
                                    if not(NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.CVBS2)):
                                        Is_Playing = False
                                    else:
                                        Is_Playing = True
                                else:
                                    Is_Playing = True
                                if(Is_Playing):
                                    video_result = 0                                
                                    i = 0                               
                                    while(i < 3):
                                        try:
                                            ## Perform grab picture
                                            if not(NOS_API.grab_picture("SCART_video")):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 6488.")
                                                    Break_Cicle = True
                                                    break
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return
                                            ## Compare grabbed and expected image and get result of comparison
                                            video_result = NOS_API.compare_pictures("SCART_video_ref", "SCART_video", "[HALF_SCREEN_576p]")
                                            video_result_1 = NOS_API.compare_pictures("SCART_video_ref1", "SCART_video", "[HALF_SCREEN_576p]")
                                        except:
                                            i = i + 1
                                            continue
                                
                                        ## Check video analysis results and update comments
                                        if (video_result >= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD or video_result_1 >= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD):
                                            ## Set test result to PASS
                                            test_result_SCART_video = True
                                            break
                                        i = i + 1
                                        
                                    if(Break_Cicle):
                                        continue
                                        
                                    if (i >= 3):
                                        TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on SCART interface.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_noise_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_noise_error_message \
                                                                            + "; V: " + str(video_result))
                                        error_codes = NOS_API.test_cases_results_info.scart_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.scart_noise_error_message
                                        NOS_API.set_error_message("Video Scart")
                                        Repeat = 2
                            
                                else:
                                    TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on SCART interface.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_freezing_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_image_freezing_error_message)
                                    error_codes = NOS_API.test_cases_results_info.scart_image_freezing_error_code
                                    error_messages = NOS_API.test_cases_results_info.scart_image_freezing_error_message
                                    NOS_API.set_error_message("Video Scart")
                                    Repeat = 2
                            else:
                                TEST_CREATION_API.write_log_to_file("No video SCART.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                                error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                                NOS_API.set_error_message("Video Scart")
                                Repeat = 2
                                
                                
                            if(test_result_SCART_video):
                                
                                NOS_API.grabber_stop_video_source()
                                time.sleep(0.5)
                                
                                
                                ## Start grabber device with audio on SCART audio source
                                TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN2)
                                time.sleep(2)
                                
                                ## Record audio from digital output (SCART)
                                TEST_CREATION_API.record_audio("SCART_audio", MAX_RECORD_AUDIO_TIME)
                                
                                #############Comparacao com referencia audio OK############################################
                                
                                ## Compare recorded and expected audio and get result of comparison
                                audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio", "[AUDIO_ANALOG]")
                                audio_result_2 = NOS_API.compare_audio("No_Right_ref", "SCART_audio", "[AUDIO_ANALOG]")
                                audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio", "[AUDIO_ANALOG]")
                                
                                if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                
                                    ## Check is audio present on channel
                                    if (TEST_CREATION_API.is_audio_present("SCART_audio")):
                                        test_result_SCART_audio = True
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                        error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                        error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                        NOS_API.set_error_message("Audio Scart") 
                                        Repeat = 2
                                else:
                                    time.sleep(3)
                                    
                                    NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                    
                                    ## Record audio from digital output (SCART)
                                    TEST_CREATION_API.record_audio("SCART_audio1", MAX_RECORD_AUDIO_TIME)
                                    
                                    ## Compare recorded and expected audio and get result of comparison
                                    audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                    audio_result_2 = NOS_API.compare_audio("No_Right_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                    audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio1", "[AUDIO_ANALOG]")
                                    
                                    if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    
                                        ## Check is audio present on channel
                                        if (TEST_CREATION_API.is_audio_present("SCART_audio1")):
                                            test_result_SCART_audio = True
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                            error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                            NOS_API.set_error_message("Audio Scart")
                                            Repeat = 2
                                    else:   
                                        try:
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                        except: 
                                            pass
                                            
                                        NOS_API.Inspection = True
                                        
                                        if (NOS_API.configure_power_switch_by_inspection()):
                                            if not(NOS_API.power_off()): 
                                                TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                NOS_API.set_error_message("Inspection")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    "",
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                            
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)

                                                return
                                            time.sleep(10)
                                            ## Power on STB with energenie
                                            if not(NOS_API.power_on()):
                                                TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                NOS_API.set_error_message("Inspection")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    "",
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                test_result = "FAIL"
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                            
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                
                                                return
                                            time.sleep(15)
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                                            
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                            NOS_API.set_error_message("Inspection")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                "",
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            test_result = "FAIL"
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                        
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                            
                                            return
                                        
                                        NOS_API.Inspection = False
                                        
                                        NOS_API.initialize_grabber()
                                        
                                        ## Start grabber device with audio on SCART audio source
                                        TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN2)
                                        time.sleep(2)
                                        
                                        ## Record audio from digital output (SCART)
                                        TEST_CREATION_API.record_audio("SCART_audio2", MAX_RECORD_AUDIO_TIME)
                                        
                                        ## Compare recorded and expected audio and get result of comparison
                                        audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio2", "[AUDIO_ANALOG]")
                                        audio_result_2 = NOS_API.compare_audio("No_Right_ref", "SCART_audio2", "[AUDIO_ANALOG]")
                                        audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio2", "[AUDIO_ANALOG]")
                                        
                                        if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                            ## Check is audio present on channel
                                            if (TEST_CREATION_API.is_audio_present("SCART_audio2")):
                                                test_result_SCART_audio = True
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                                error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                                error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                                NOS_API.set_error_message("Audio Scart") 
                                                Repeat = 2
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SCART interface.")
                                            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code  \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_code  \
                                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_message)
                                            error_codes = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_code
                                            error_messages = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_message
                                            NOS_API.set_error_message("Audio Scart") 
                                            Repeat = 2
                                        
                            ######################################################################## Telnet Test #################################################################################             
                                        
                                if(test_result_SCART_audio): 
                                    NOS_API.give_me_give_me_give_me_a_time_after_finish("Análise Interfaces") 
                                    cmd = 'show cable modem ' + NOS_API.test_cases_results_info.mac_using_barcode
                                    #Get start time
                                    startTime = time.localtime()
                                    sid = NOS_API.get_session_id()
                                    TEST_CREATION_API.write_log_to_file(str(sid))
                                    while (True):
                                        
                                        response = NOS_API.send_cmd_to_telnet(sid, cmd)
                                        TEST_CREATION_API.write_log_to_file("response:" + str(response))
                                        if(response != None):
                                            if(response.find("Error:") != -1):
                                                error_command_telnet = True
                                                break
                                            if(response == "connect timed out"):
                                                NOS_API.quit_session(sid)
                                                time.sleep(1)
                                                sid = NOS_API.get_session_id()
                                                response = NOS_API.send_cmd_to_telnet(sid, cmd)
                                                TEST_CREATION_API.write_log_to_file("response:" + str(response))
                                                if(response != None):
                                                    if(response.find("Error:") != -1):
                                                        error_command_telnet = True
                                                        break
                                                    if(response == "connect timed out"):
                                                        NOS_API.set_error_message("Telnet timeout")
                                                        TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                                        error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                        error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                            
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = ""    
                                                    
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                    
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)  
                                                        return
                                                    if(response != "BUSY"):
                                                        stb_state = NOS_API.is_stb_operational(response)
                                                        break       
                                                else:
                                                    NOS_API.set_error_message("Telnet timeout")
                                                    TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                                    TEST_CREATION_API.write_log_to_file("Resposta em branco scm")
                                                    
                                                    error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                    error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                        
                                                    NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    report_file = ""    
                                                
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)  
                                                    return
                                                    
                                            if(response != "BUSY"):
                                                stb_state = NOS_API.is_stb_operational(response)
                                                break 
                                        else:
                                            NOS_API.set_error_message("Telnet timeout")
                                            TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                            TEST_CREATION_API.write_log_to_file("Resposta em branco scm")
                                            
                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                
                                            NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = ""    
                                        
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)  
                                            return
                                          
                                        time.sleep(5)
                                            
                                        #Get current time
                                        currentTime = time.localtime()
                                        if((time.mktime(currentTime) - time.mktime(startTime)) > NOS_API.MAX_WAIT_TIME_RESPOND_FROM_TELNET):
                                            NOS_API.set_error_message("Telnet timeout")
                                            TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                            TEST_CREATION_API.write_log_to_file("Excedeu tempo no verbose. Resposta: " + response)
                                            error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                            error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                
                                            NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = ""    
                                        
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)  
                                            return
                                    
                                    if(error_command_telnet == False):
                                        if(stb_state == True):                                       
                                            cmd = 'show cable modem ' + NOS_API.test_cases_results_info.mac_using_barcode + ' verbose'
                                            startTime = time.localtime()
                                            while (True):
                                        
                                                response = NOS_API.send_cmd_to_telnet(sid, cmd)
                                                TEST_CREATION_API.write_log_to_file("response:" + str(response))  

                                                if(response != None and response != "BUSY" and response != "connect timed out"):
                                                    data = NOS_API.parse_telnet_cmd1(response)
                                                    break
                                                if(response == None):
                                                    NOS_API.set_error_message("Telnet timeout")
                                                    TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                                    
                                                    error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                    error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                        
                                                    NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    report_file = ""    
                                                    
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)  
                                                    return
                                                if(response == "connect timed out"):
                                                    NOS_API.quit_session(sid)
                                                    response = NOS_API.send_cmd_to_telnet(sid, cmd)
                                                    TEST_CREATION_API.write_log_to_file("response:" + str(response))                
                                                    
                                                    if(response != None and response != "BUSY" and response != "connect timed out"):
                                                        data = NOS_API.parse_telnet_cmd1(response)
                                                        break
                                                    if(response == None):
                                                        NOS_API.set_error_message("Telnet timeout")
                                                        TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                                        
                                                        error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                        error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                            
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = ""    
                                                        
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)  
                                                        return
                                                    if(response == "connect timed out"):
                                                        NOS_API.set_error_message("Telnet timeout")
                                                        TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                                        error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                        error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                            
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = ""    
                                                    
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                    
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)  
                                                        return
                                            
                                                time.sleep(5)
                                                    
                                                #Get current time
                                                currentTime = time.localtime()
                                                if((time.mktime(currentTime) - time.mktime(startTime)) > NOS_API.MAX_WAIT_TIME_RESPOND_FROM_TELNET):
                                                    #NOS_API.quit_session(sid)
                                                    NOS_API.set_error_message("Telnet timeout")
                                                    TEST_CREATION_API.write_log_to_file("Didn't establish/Lost Telnet communication with CMTS")
                                                    TEST_CREATION_API.write_log_to_file("Excedeu tempo no verbose. Resposta: " + response)
                                                    
                                                    error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                                    error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                                        
                                                    NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    report_file = ""    
                                                    
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)  
                                                    return                                                
                                                
                                            if (data[1] == "Operational"):
                                                NOS_API.test_cases_results_info.ip = data[0]
                                                Telnet_Test_Result = True
                                                #test_result = "PASS"
                                            else:           
                                                TEST_CREATION_API.write_log_to_file("STB State is not operational")
                                                NOS_API.set_error_message("CM Docsis")
                                                error_codes = NOS_API.test_cases_results_info.ip_error_code
                                                error_messages = NOS_API.test_cases_results_info.ip_error_message  
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.ip_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.ip_error_message)
                                                Repeat = 2
                                        else:
                                            TEST_CREATION_API.write_log_to_file("STB State is not operational")
                                            NOS_API.set_error_message("CM Docsis")
                                            error_codes = NOS_API.test_cases_results_info.ip_error_code
                                            error_messages = NOS_API.test_cases_results_info.ip_error_message  
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.ip_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.ip_error_message)
                                            Repeat = 2
                                    else:
                                        NOS_API.set_error_message("Telnet timeout")
                                        TEST_CREATION_API.write_log_to_file("Error on Telnet communication")
                                        TEST_CREATION_API.write_log_to_file("Outro Erro.")
                                        
                                        error_codes = NOS_API.test_cases_results_info.cmts_error_code
                                        error_messages = NOS_API.test_cases_results_info.cmts_error_message  
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.cmts_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.cmts_error_message)
                                        Repeat = 2
                                                                                
                                    NOS_API.quit_session(sid)   
        
                            ######################################################################## Button/Led's Test #################################################################################                                     
                                    
                                    if (Telnet_Test_Result):
                                        NOS_API.give_me_give_me_give_me_a_time_after_finish("Telnet") 
                                        NOS_API.grabber_stop_audio_source()
                                        time.sleep(1)
                                        
                                        ## Start grabber device with video on default video source
                                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                        TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
        
                                        TEST_CREATION_API.send_ir_rc_command("[PLAY_CONTENT_FROM_HDD]")
                                        if not(NOS_API.grab_picture("HDD_menu")):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7040.")
                                                continue
                                            else:
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                end_time)
                                            
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                        
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                        
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                return
        
                                        if(TEST_CREATION_API.compare_pictures("HDD_Menu_ref", "HDD_menu", "[HDD_Menu]") or TEST_CREATION_API.compare_pictures("HDD_Menu1_ref", "HDD_menu", "[HDD_Menu]")):
                                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                                            if not(NOS_API.grab_picture("HDD_menu_1")):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7087.")
                                                    continue
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return
        
                                            if(TEST_CREATION_API.compare_pictures("HDD_Menu_ref", "HDD_menu_1", "[HDD_Menu]") or TEST_CREATION_API.compare_pictures("HDD_Menu1_ref", "HDD_menu_1", "[HDD_Menu]")):
                                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                                if not(NOS_API.grab_picture("HDD_menu_2")):
                                                    if (Repeat == 0):
                                                        Repeat = Repeat + 1
                                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                                        else:
                                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7134.")
                                                        continue
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                        
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                    
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                                
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                                
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        return
        
                                                if(TEST_CREATION_API.compare_pictures("HDD_Menu_ref", "HDD_menu_2", "[HDD_Menu]") or TEST_CREATION_API.compare_pictures("HDD_Menu1_ref", "HDD_menu_2", "[HDD_Menu]")):
                                                    TEST_CREATION_API.write_log_to_file("STB doesn't receive IR commands.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                                                    NOS_API.set_error_message("IR")
                                                    error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                                    error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
        
                                                    return
                                        else:
                                            if(TEST_CREATION_API.compare_pictures("No_Content_ref", "HDD_menu", "[No_Content]") or TEST_CREATION_API.compare_pictures("No_content_ref2", "HDD_menu", "[No_Content]")):
                                                NOS_API.test_cases_results_info.recording_started = False
                                                TEST_CREATION_API.write_log_to_file("Recording is not started")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recording_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.recording_error_message)
                                                error_codes = NOS_API.test_cases_results_info.recording_error_code
                                                error_messages = NOS_API.test_cases_results_info.recording_error_message
                                                NOS_API.set_error_message("HDD")
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                
                                                return
                                            compare_result = NOS_API.wait_for_multiple_pictures(["Recording_Active_ref", "Recording_Active_new_ref"], 30, ["[Menu_Arquivo]", "[Menu_Arquivo]"], [NOS_API.thres, NOS_API.thres])
                                            if (compare_result == -1 or compare_result == -2):
                                                if(TEST_CREATION_API.compare_pictures("No_Content_ref", "HDD_menu", "[No_Content]") or TEST_CREATION_API.compare_pictures("No_content_ref2", "HDD_menu", "[No_Content]")):
                                                    NOS_API.test_cases_results_info.recording_started = False
                                                    TEST_CREATION_API.write_log_to_file("Recording is not started")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recording_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.recording_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.recording_error_code
                                                    error_messages = NOS_API.test_cases_results_info.recording_error_message
                                                    NOS_API.set_error_message("HDD")
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                    
                                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                                    
                                                    return
                                                TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                                TEST_CREATION_API.send_ir_rc_command("[PLAY_CONTENT_FROM_HDD]")
                                                if not(NOS_API.grab_picture("HDD_menu")):
                                                    if (Repeat == 0):
                                                        Repeat = Repeat + 1
                                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                                        else:
                                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 5371.")
                                                        continue
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                        
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                    
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                                
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                                
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        return
                                                
                                                if(TEST_CREATION_API.compare_pictures("HDD_Menu_ref", "HDD_menu", "[HDD_Menu]")):
                                                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Couldn't navigate to HDD Menu")
                                                    NOS_API.set_error_message("Navegação")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                    error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                    error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    report_file = ""    
                                                    
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
            
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    return
                                            else:
                                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                                if not(NOS_API.grab_picture("HDD_menu_1")):
                                                    if (Repeat == 0):
                                                        Repeat = Repeat + 1
                                                        if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                            NOS_API.test_cases_results_info.DidUpgrade = 5
                                                        else:
                                                            NOS_API.test_cases_results_info.DidUpgrade = 4
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7087.")
                                                        continue
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                        NOS_API.set_error_message("Reboot")
                                                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                        
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                    
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                                                                
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                                
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        return
            
                                                if(TEST_CREATION_API.compare_pictures("HDD_Menu_ref", "HDD_menu_1", "[HDD_Menu]") or TEST_CREATION_API.compare_pictures("HDD_Menu1_ref", "HDD_menu_1", "[HDD_Menu]")):
                                                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                                                    if not(NOS_API.grab_picture("HDD_menu_2")):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7134.")
                                                            continue
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                        
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                                    
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                                                    
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            return
            
                                                    if(TEST_CREATION_API.compare_pictures("HDD_Menu_ref", "HDD_menu_2", "[HDD_Menu]") or TEST_CREATION_API.compare_pictures("HDD_Menu1_ref", "HDD_menu_2", "[HDD_Menu]")):
                                                        TEST_CREATION_API.write_log_to_file("STB doesn't receive IR commands.")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                                                        NOS_API.set_error_message("IR")
                                                        error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                                        error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
            
                                                        return
                                        time.sleep(8)
                                        if not (NOS_API.is_signal_present_on_video_source()):
                                            if (Repeat == 0):
                                                Repeat = Repeat + 1
                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                else:
                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7350.")
                                                continue
                                            else:
                                                #NOS_API.display_custom_dialog("Perdeu sinal a meio do teste", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                NOS_API.set_error_message("Reboot")
                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                test_result = "FAIL"
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                        
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                    
                                            
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                            
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                return
                                            
                                        ## Record video with duration of recording (5 seconds)
                                        NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
        
                                        ## Instance of PQMAnalyse type
                                        pqm_analyse = TEST_CREATION_API.PQMAnalyse()
        
                                        ## Set what algorithms should be checked while analyzing given video file with PQM.
                                        # Attributes are set to false by default.
                                        pqm_analyse.black_screen_activ = True
                                        pqm_analyse.blocking_activ = True
                                        pqm_analyse.freezing_activ = True
        
                                        # Name of the video file that will be analysed by PQM.
                                        pqm_analyse.file_name = "video"
        
                                        ## Analyse recorded video
                                        analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
        
                                        if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                            pqm_analyse_check = False
                                            TEST_CREATION_API.write_log_to_file("Fail on PQM Analyses. Black Screen was detected")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message)
                                            NOS_API.set_error_message("HDD")       
                                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message
        
                                        if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                            pqm_analyse_check = False
                                            TEST_CREATION_API.write_log_to_file("Fail on PQM Analyses. Blocking was detected")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                                            NOS_API.set_error_message("HDD")
                                            if (error_codes == ""):
                                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                                            else:
                                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                                            
                                            if (error_messages == ""):
                                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                                            else:
                                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
        
                                        if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                            pqm_analyse_check = False
                                            TEST_CREATION_API.write_log_to_file("Fail on PQM Analyses. Frezzing was detected")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                                            NOS_API.set_error_message("HDD")
                                            if (error_codes == ""):
                                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                            else:
                                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                            
                                            if (error_messages == ""):
                                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                            else:
                                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                        
                                        if not(pqm_analyse_check): 
                                            NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                            
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                        
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                    
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                                    
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            return 
        
                                        ## Check if video is playing (check if video is not freezed)
                                        if not(NOS_API.is_video_playing()):
                                            time.sleep(5)
                                            if not(NOS_API.is_video_playing()):
                                                Is_Playing = False
                                            else:
                                                Is_Playing = True
                                        else:
                                            Is_Playing = True
                                        if(Is_Playing):
                                        
                                            video_result = 0
                                            
                                            ## Perform grab picture
                                            if not(NOS_API.grab_picture("recorded_content")):
                                                if (Repeat == 0):
                                                    Repeat = Repeat + 1
                                                    if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                        NOS_API.test_cases_results_info.DidUpgrade = 5
                                                    else:
                                                        NOS_API.test_cases_results_info.DidUpgrade = 4
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7487.")
                                                    continue
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                    NOS_API.set_error_message("Reboot")
                                                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                    
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                                            
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    return
                                                
                                            ## Compare grabbed and expected image and get result of comparison
                                            video_result = NOS_API.compare_pictures("recorded_content_ref", "recorded_content", "[HALF_SCREEN]")
                                            video_result_1 = NOS_API.compare_pictures("recorded_content_ref1", "recorded_content", "[HALF_SCREEN]")
                                            video_result_2 = NOS_API.compare_pictures("recorded_content_ref2", "recorded_content", "[HALF_SCREEN]")
        
                                            ## Check video analysis results and update comments
                                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                if (analysed_video): 
                                                    ## Set test result to PASS           
                                                    VIDEO_RECORD_Result = True
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.grabber_error_code
                                                    error_messages = NOS_API.test_cases_results_info.grabber_error_message
                                                    NOS_API.set_error_message("Inspection")
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
                                            
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    return 
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Recorded video is not reproduced correctly on HDMI 720p interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                                    + "; V: " + str(video_result))
                                                NOS_API.set_error_message("HDD") 
                                                error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                                error_messages =  NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                                Repeat = 2
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Recorded video is not playing on HDMI 720p interface.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message \
                                                                                    + "; Recorded video is not playing")
                                            error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                            error_messages =  NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                            NOS_API.set_error_message("HDD") 
                                            Repeat = 2
                                                                                                                    
                                        ################################################################ Audio Record Test ############################################################################
                                        
                                        if(VIDEO_RECORD_Result):
                                            ## Record audio from digital output (HDMI)
                                            TEST_CREATION_API.record_audio("HDMI_audio_rec", MAX_RECORD_AUDIO_TIME)
        
                                            ## Compare recorded and expected audio and get result of comparison
                                            audio_result1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_rec")
        
                                            if (audio_result1 > TEST_CREATION_API.AUDIO_THRESHOLD):
                                            
                                                ## Record audio from digital output (HDMI)
                                                TEST_CREATION_API.record_audio("HDMI_audio_rec", MAX_RECORD_AUDIO_TIME)
        
                                                ## Compare recorded and expected audio and get result of comparison
                                                audio_result1 = NOS_API.compare_audio("No_Both_ref", "HDMI_audio_rec")
        
                                            if (audio_result1 < TEST_CREATION_API.AUDIO_THRESHOLD):
        
                                                ## Check is audio present on channel
                                                if (TEST_CREATION_API.is_audio_present("HDMI_audio_rec")):
                                                    ## Set test result to PASS
                                                    AUDIO_RECORD_Result = True
                                                else:                                 
                                                    TEST_CREATION_API.write_log_to_file("Audio is not present on hdmi 720p interface.")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message \
                                                                                        + "; Audio is not present on hdmi_576p interface")
                                                    error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code
                                                    error_messages = NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message
                                                    Repeat = 2
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.recorded_content_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.recorded_content_nok_error_message)
                                                NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                                        + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                                error_codes = NOS_API.test_cases_results_info.recorded_content_nok_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                                error_messages = NOS_API.test_cases_results_info.recorded_content_nok_error_message + " " +  NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                                Repeat = 2
                                                
                                            if(AUDIO_RECORD_Result):
                                                NOS_API.give_me_give_me_give_me_a_time_after_finish("Play e Análise da Gravação")
                                                #if not(NOS_API.display_custom_dialog("O Led Rede est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                #    TEST_CREATION_API.write_log_to_file("Led Rede NOK")
                                                #    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.led_net_nok_error_code \
                                                #                                    + "; Error message: " + NOS_API.test_cases_results_info.led_net_nok_error_message)
                                                #    NOS_API.set_error_message("Led's")
                                                #    error_codes = NOS_API.test_cases_results_info.led_net_nok_error_code
                                                #    error_messages = NOS_API.test_cases_results_info.led_net_nok_error_message
                                                #    test_result = "FAIL"
                                                #    
                                                #    NOS_API.add_test_case_result_to_file_report(
                                                #                    test_result,
                                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                                #                    error_codes,
                                                #                    error_messages)
                                                #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                #    report_file = ""
                                                #    if (test_result != "PASS"):
                                                #        report_file = NOS_API.create_test_case_log_file(
                                                #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                #                        NOS_API.test_cases_results_info.nos_sap_number,
                                                #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                #                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                #                        end_time)
                                                #        NOS_API.upload_file_report(report_file)
                                                #        NOS_API.test_cases_results_info.isTestOK = False
                                                #
                                                #
                                                #    ## Update test result
                                                #    TEST_CREATION_API.update_test_result(test_result)
                                                #    
                                                #    ## Return DUT to initial state and de-initialize grabber device
                                                #    NOS_API.deinitialize()
                                                #    
                                                #    NOS_API.send_report_over_mqtt_test_plan(
                                                #        test_result,
                                                #        end_time,
                                                #        error_codes,
                                                #        report_file)
                                                #
                                                #    return
                                                if not(NOS_API.display_custom_dialog("Ventoinha?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                    TEST_CREATION_API.write_log_to_file("FAN is not running")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.fan_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.fan_error_message)
                                                    NOS_API.set_error_message("Ventoinha")
                                                    error_codes = NOS_API.test_cases_results_info.fan_error_code
                                                    error_messages = NOS_API.test_cases_results_info.fan_error_message
                                                    test_result = "FAIL"
                                                    
                                                    NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                    report_file = ""
                                                    if (test_result != "PASS"):
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                    
                                                    return
                                                NOS_API.display_custom_dialog("Pressione no bot\xe3o 'Power'", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) 
                                                if not(NOS_API.wait_for_no_signal_present(20)):
                                                    NOS_API.display_custom_dialog("Pressione no bot\xe3o 'Power'", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) 
                                                    if not(NOS_API.wait_for_no_signal_present(20)):
                                                        TEST_CREATION_API.write_log_to_file("Power button NOK")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_button_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_button_nok_error_message)
                                                        NOS_API.set_error_message("Botões")   
                                                        error_codes = NOS_API.test_cases_results_info.power_button_nok_error_code
                                                        error_messages = NOS_API.test_cases_results_info.power_button_nok_error_message  
                                                        test_result = "FAIL"
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
            
                                                        return
                                                if (NOS_API.display_custom_dialog("O Led Vermelho est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                    if (NOS_API.display_custom_dialog("O Display est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                                        NOS_API.give_me_give_me_give_me_a_time_after_finish("Perguntas")
                                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                        time.sleep(10)
                                                        if not(NOS_API.is_signal_present_on_video_source()):
                                                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                            time.sleep(10)
                                                            if not(NOS_API.is_signal_present_on_video_source()):
                                                                NOS_API.display_custom_dialog("Não recebeu comando Power", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                                                TEST_CREATION_API.write_log_to_file("STB doesn't receive IR commands.")
                                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                                                                NOS_API.set_error_message("IR")
                                                                error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                                                error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                                                                test_result = "FAIL"
                                                                
                                                                NOS_API.add_test_case_result_to_file_report(
                                                                                test_result,
                                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                                error_codes,
                                                                                error_messages)
                                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                                report_file = ""
                                                                if (test_result != "PASS"):
                                                                    report_file = NOS_API.create_test_case_log_file(
                                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                    NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                    end_time)
                                                                    NOS_API.upload_file_report(report_file)
                                                                    NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                                                ## Update test result
                                                                TEST_CREATION_API.update_test_result(test_result)
                                                                
                                                                ## Return DUT to initial state and de-initialize grabber device
                                                                NOS_API.deinitialize()
                                                                
                                                                NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
        
                                                                return
                                                            else:
                                                                test_result_ButtonLeds = True
                                                        else:
                                                            test_result_ButtonLeds = True
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("Display NOK")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.display_nok_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.display_nok_error_message)
                                                        NOS_API.set_error_message("Display")
                                                        error_codes = NOS_API.test_cases_results_info.display_nok_error_code
                                                        error_messages = NOS_API.test_cases_results_info.display_nok_error_message
                                                        Repeat = 2
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Led POWER Red NOK")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.led_power_red_nok_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.led_power_red_nok_error_message)
                                                    NOS_API.set_error_message("Led's")
                                                    error_codes = NOS_API.test_cases_results_info.led_power_red_nok_error_code
                                                    error_messages = NOS_API.test_cases_results_info.led_power_red_nok_error_message
                                                    Repeat = 2
                                                
                                                if(test_result_ButtonLeds):
                                                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                                                    time.sleep(1)
                                                    TEST_CREATION_API.send_ir_rc_command("[Factory_Reset]")
                                                    if not(NOS_API.grab_picture("Factory_Reset")):
                                                        if (Repeat == 0):
                                                            Repeat = Repeat + 1
                                                            if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                NOS_API.test_cases_results_info.DidUpgrade = 5
                                                            else:
                                                                NOS_API.test_cases_results_info.DidUpgrade = 4
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7844.")
                                                            continue
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                            NOS_API.set_error_message("Reboot")
                                                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                            
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                            
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                        
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                                                                    
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                                                    
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            
                                                            return
                                                    
                                                    video_result = NOS_API.compare_pictures("Factory_Reset_ref", "Factory_Reset", "[Factory_Reset]")
                                                    video_result_1 = NOS_API.compare_pictures("Factory_Reset_Black_ref", "Factory_Reset", "[Factory_Reset]")
                                                    
                                                    if not(video_result >= NOS_API.thres or video_result_1 >= NOS_API.thres):
                                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX_NEW]")
                                                        TEST_CREATION_API.send_ir_rc_command("[CH_1]")
                                                        TEST_CREATION_API.send_ir_rc_command("[Factory_Reset_Slow]")
                                                        if not(NOS_API.grab_picture("Factory_Reset_1")):
                                                            if (Repeat == 0):
                                                                Repeat = Repeat + 1
                                                                if(NOS_API.test_cases_results_info.DidUpgrade == 1):
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 5
                                                                else:
                                                                    NOS_API.test_cases_results_info.DidUpgrade = 4
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot. Line 7896.")
                                                                continue
                                                            else:
                                                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                                                NOS_API.set_error_message("Reboot")
                                                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                                                
                                                                NOS_API.add_test_case_result_to_file_report(
                                                                            test_result,
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                                            error_codes,
                                                                            error_messages)
                                                
                                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                                report_file = NOS_API.create_test_case_log_file(
                                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                                                end_time)
                                                            
                                                                NOS_API.upload_file_report(report_file)
                                                                NOS_API.test_cases_results_info.isTestOK = False
                                                                                        
                                                                NOS_API.send_report_over_mqtt_test_plan(
                                                                        test_result,
                                                                        end_time,
                                                                        error_codes,
                                                                        report_file)
                                                                        
                                                                ## Update test result
                                                                TEST_CREATION_API.update_test_result(test_result)
                                                                
                                                                ## Return DUT to initial state and de-initialize grabber device
                                                                NOS_API.deinitialize()
                                                                
                                                                return
                                                        
                                                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                        
                                                        if (video_height == "720"):
                                                            video_result_2 = NOS_API.compare_pictures("Factory_Reset_ref", "Factory_Reset_1", "[Factory_Reset]")
                                                            video_result_3 = NOS_API.compare_pictures("Factory_Reset_Black_ref", "Factory_Reset_1", "[Factory_Reset]")
                                                            video_result_4 = 0
                                                        elif (video_height == "1080"):
                                                            video_result_2 = 0
                                                            video_result_3 = 0
                                                            video_result_4 = NOS_API.compare_pictures("Factory_Reset_1080_ref", "Factory_Reset_1", "[Factory_Reset_1080]")
                                                            
                                                        if not(video_result_2 >= NOS_API.thres or video_result_3 >= NOS_API.thres or video_result_4 >= NOS_API.thres):
                                                            TEST_CREATION_API.write_log_to_file("Navigation to resumo screen failed")
                                                            NOS_API.set_error_message("Navegação")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                                                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                            error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                    test_result,
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                                    error_codes,
                                                                    error_messages)
                                                        
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                            report_file = ""    
                                                            
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
        
                                                            ## Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
        
                                                            ## Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            return
                                                        else:
                                                            TEST_CREATION_API.send_ir_rc_command("[Factory_Reset2]")
                                                    else:
                                                        TEST_CREATION_API.send_ir_rc_command("[Factory_Reset2]")
                                                    
                                                    if (NOS_API.wait_for_no_signal_present(20)):
                                                        time.sleep(15)           
                                                        NOS_API.configure_power_switch_by_inspection()
                                                        if not(NOS_API.power_off()): 
                                                            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                                            
                                                            NOS_API.set_error_message("POWER SWITCH")
                                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                                            error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                                                            error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                                                            # Return DUT to initial state and de-initialize grabber device
                                                            NOS_API.deinitialize()
                                                            NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                        
                                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                                                        end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            
                                                            NOS_API.send_report_over_mqtt_test_plan(
                                                                    test_result,
                                                                    end_time,
                                                                    error_codes,
                                                                    report_file)
                                                            
                                                            # Update test result
                                                            TEST_CREATION_API.update_test_result(test_result)
                                                            
                                                            return 
                                                        try:
                                                            Send_Serial_Key("d", "feito")
                                                        except:
                                                            TEST_CREATION_API.write_log_to_file("USBs are not disabled")
                                                        test_result = "PASS"
                                                        Repeat = 2
                                                        NOS_API.give_me_give_me_give_me_a_time_after_finish("FR")
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("Does not do Factory Reset")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                                        NOS_API.set_error_message("Factory Reset")
                                                        error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                                        error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
                                                        test_result = "FAIL"
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                                        report_file = ""
                                                        if (test_result != "PASS"):
                                                            report_file = NOS_API.create_test_case_log_file(
                                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                                            end_time)
                                                            NOS_API.upload_file_report(report_file)
                                                            NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)
        
                                                        return
                
            System_Failure = 2
            
        except Exception as error:
            if(System_Failure == 0):
                System_Failure = System_Failure + 1 
                NOS_API.Inspection = True
                if(System_Failure == 1):
                    try:
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                    try:
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
    
                        return
                    time.sleep(10)
                    ## Power on STB with energenie
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        test_result = "FAIL"
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                        return
                    time.sleep(10)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    NOS_API.set_error_message("Inspection")
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                    report_file = ""
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    test_result = "FAIL"
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                    
                    return
                
                NOS_API.Inspection = False
            else:
                test_result = "FAIL"
                TEST_CREATION_API.write_log_to_file(error)
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                NOS_API.set_error_message("Inspection")
                System_Failure = 2 
        ####################################################################################################################################################################################################################
   
    NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    str(snr_value) + " " + str(ber_value) + " - - " + str(tx_value) + " " + str(rx_value) + " " + str(downloadstream_snr_value) + " - - - - - " + str(cas_id_number) + " " + str(sw_version) + " - " + str(sc_number) + " - " + str(modulation) + " " + str(frequencia) + " -",
                    ">50<70 <1.0E-6 - - <52 >-10<10 >=34 - - - - - - - - - - - - -",
                    error_codes,
                    error_messages)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    report_file = ""    
    
    report_file = NOS_API.create_test_case_log_file(
                    NOS_API.test_cases_results_info.s_n_using_barcode,
                    NOS_API.test_cases_results_info.nos_sap_number,
                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                    NOS_API.test_cases_results_info.mac_using_barcode,
                    end_time)
    NOS_API.upload_file_report(report_file)
    NOS_API.test_cases_results_info.isTestOK = False
    
    NOS_API.send_report_over_mqtt_test_plan(
            test_result,
            end_time,
            error_codes,
            report_file)

    ## Update test result
    TEST_CREATION_API.update_test_result(test_result)

    ## Return DUT to initial state and de-initialize grabber device
    NOS_API.deinitialize()