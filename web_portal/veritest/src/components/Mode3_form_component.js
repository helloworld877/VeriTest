"use client";
import { useState, useEffect } from "react";
import DropdownFormControl from "@/components/Mode3_dropdown_component";

const MyForm = (responseData, ready) => {
  // constants
  // circuit Types
  const circuitTypes = [
    "adder",
    "decoder",
    "encoder",
    "mux",
    "not",
    "seg",
    "and",
    "nand",
    "or",
    "nor",
    "xor",
    "xnor",
  ];
  const initialInputOptions = [];
  const initialOutputOptions = ["Output A", "Output B", "Output C"];
  // States
  const [inputOptions, setInputOptions] = useState([]);
  const [selectedInputs, setSelectedInputs] = useState([]);

  const [outputOptions, setOutputOptions] = useState(initialOutputOptions);
  const [selectedOutputs, setSelectedOutputs] = useState([]);

  const [circuitType, setCircuitType] = useState("");

  const [modelName, setModelName] = useState("");
  /////////////////////////////////////////
  // gate circuit type
  const [gateTypeOperationType, setGateTypeOperationType] = useState("");
  /////////////////////////////////////////

  // state handlers
  const handleSelectInput = (option) => {
    setInputOptions(inputOptions.filter((opt) => opt !== option));
    setSelectedInputs([...selectedInputs, option]);
  };

  const handleRemoveInput = (option) => {
    setSelectedInputs(selectedInputs.filter((item) => item !== option));
    setInputOptions([...inputOptions, option]);
  };

  const handleSelectOutput = (option) => {
    setOutputOptions(outputOptions.filter((opt) => opt !== option));
    setSelectedOutputs([...selectedOutputs, option]);
  };

  const handleRemoveOutput = (option) => {
    setSelectedOutputs(selectedOutputs.filter((item) => item !== option));
    setOutputOptions([...outputOptions, option]);
  };

  const handleCircuitTypeChange = (e) => {
    setCircuitType(e.target.value);
  };
  const handleModelNameChange = (e) => {
    setModelName(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here, e.g., send data to a server or validate the form
    console.log("Form submitted with selected inputs:", selectedInputs);
    console.log("Form submitted with selected outputs:", selectedOutputs);
  };

  /////////////////////////////////////////
  // gate circuit type
  const handleGateTypeOperationTypeChange = (e) => {
    setGateTypeOperationType(e.target.value);
  };
  /////////////////////////////////////////
  // code runs once in the start to fill out form fields
  useEffect(() => {
    // Code to run once when the component mounts
    console.log("Component mounted");

    let data = responseData.responseData;
    console.log(data);
    // checking on the type

    data.inputs.map((input, index) => {
      console.log(input);
      const newItem = `name:${input.name} size:${input.size}`;
      console.log(selectedInputs);
      // Check if the newItem already exists in selectedInputs
      setSelectedInputs((prevSet) => {
        const newSet = new Set(prevSet);
        newSet.add(newItem);
        return [...newSet];
      });
    });

    if (["and", "nand", "or", "nor", "xor", "xnor"].includes(data.type)) {
    }
  }, [ready]);

  /////////////////////////////////////////

  return (
    <form onSubmit={handleSubmit}>
      <h1 className="text-center mt-4">Specifications</h1>
      <div className="row">
        <div className="col">
          <div class="input-group input-group-md mb-3">
            <span class="input-group-text" id="inputGroup-sizing-sm">
              Model Name
            </span>
            <input
              type="text"
              class="form-control"
              value={modelName}
              onChange={handleModelNameChange}
            />
          </div>
        </div>
        <div className="col">
          <div className="input-group mb-3">
            <label className="input-group-text" for="circuit_type">
              Type
            </label>
            <select
              className="form-select"
              id="circuit_type"
              value={circuitType}
              onChange={handleCircuitTypeChange}
            >
              <option value="" disabled>
                Choose...
              </option>
              {circuitTypes.map((option, index) => (
                <option key={index} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col">
          <DropdownFormControl
            label="Inputs"
            options={inputOptions}
            selectedItems={selectedInputs}
            onSelect={handleSelectInput}
            onRemove={handleRemoveInput}
          />
        </div>
        <div className="col">
          <DropdownFormControl
            label="Outputs"
            options={outputOptions}
            selectedItems={selectedOutputs}
            onSelect={handleSelectOutput}
            onRemove={handleRemoveOutput}
          />
        </div>
      </div>
      {/* gate specification fields */}
      {["and", "nand", "or", "nor", "xor", "xnor"].includes(circuitType) && (
        <div>
          <hr />
          <div className="input-group mb-3">
            <label className="input-group-text" for="gate_operation_type">
              Operation Type
            </label>
            <select
              className="form-select"
              id="gate_operation_type"
              value={gateTypeOperationType}
              onChange={handleGateTypeOperationTypeChange}
            >
              <option value="" disabled>
                Choose...
              </option>

              <option value="logical">logical</option>
              <option value="bitwise">bitwise</option>
            </select>
          </div>
        </div>
      )}

      <div className="mt-3">
        <button type="submit" className="btn btn-success">
          Submit
        </button>
      </div>
    </form>
  );
};

export default MyForm;
