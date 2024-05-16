#!/bin/bash

# Define the Verilog file path as a command-line argument
verilog_file="$1"

# Check if the file path is provided
if [[ -z "$verilog_file" ]]; then
    echo "Error: No Verilog file path provided."
    exit 1
fi

# Check if the file exists
if [[ ! -f "$verilog_file" ]]; then
    echo "Error: File '$verilog_file' does not exist."
    exit 1
fi


# TODO: I don't have quartus
# Call synthesizer.bash with the Verilog file
# synthesizer_output=$(./synthesizer.bash "$verilog_file")

# # Check for failure in synthesizer.ps1
# if [[ "$synthesizer_output" == "compilation failed" || "$synthesizer_output" == "synthesizability check failed" ]]; then
#     echo "Synthesizer failed: $synthesizer_output"
#     exit 1
# fi

# Call encode_test_sample.bash with the Verilog file as an argument
encode_output=$(bash $VERITEST_HOME/Mode_3/encode_test_sample.bash "$verilog_file")

# Check for failure in encode_test_sample.bash
if [[ "$encode_output" != "success" ]]; then
    echo "Encoding failed: $encode_output"
    exit 1
fi

# Change directory to the "final_model_utils" folder
cd final_model_utils || { echo "Failed to change directory to final_model_utils"; exit 1; }

# Call Infer_GNN.bash
infer_output=$(bash $VERITEST_HOME/Mode_3/Infer_GNN.bash)

# Check for failure in Infer_GNN.bash
if [[ "$infer_output" != "Success: Prediction saved in 'pred.txt'" ]]; then
    echo "Inference failed: $infer_output"
    exit 1
fi

# If all steps succeeded, return success
echo "Success: Prediction saved in 'pred.txt'"
