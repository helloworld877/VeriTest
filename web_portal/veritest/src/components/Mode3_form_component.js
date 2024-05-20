"use client";
import { useState, useEffect } from "react";
import DropdownFormControl from "@/components/Mode3_dropdown_component";
import axios from "axios";

const MyForm = ({ responseData, ready, file }) => {
  // helper functions
  function parseStringToObject(str) {
    const obj = {};
    const pairs = str.split(" ");

    pairs.forEach((pair) => {
      const [key, value] = pair.split(":");
      obj[key] = isNaN(value) ? value : Number(value);
    });

    return obj;
  }
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

    if (["and", "nand", "or", "nor", "xor", "xnor"].includes(circuitType)) {
      var requestData = {
        model_name: `${modelName}`,
        type: `${circuitType}`,
        operation_type: `${gateTypeOperationType}`,
        inputs: [],
        output: "",
      };

      selectedInputs.map((input, index) => {
        let result = parseStringToObject(input);
        requestData.inputs.push(result);
      });
      requestData.output = selectedOutputs[0];

      // console.log(file);
      const formData = new FormData();
      formData.append("json", JSON.stringify(requestData));
      formData.append("vFile", file);

      axios
        .post("http://localhost:5000/submit_prediction", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
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
    // console.log(file);
    let data = responseData;

    // checking on the type

    setModelName(data["model_name"]);
    setCircuitType(data.type);

    data.inputs.map((input, index) => {
      const newItem = `name:${input.name} size:${input.size}`;

      // Check if the newItem already exists in selectedInputs
      setSelectedInputs((prevSet) => {
        const newSet = new Set(prevSet);
        newSet.add(newItem);
        return [...newSet];
      });
    });

    if (["and", "nand", "or", "nor", "xor", "xnor"].includes(data.type)) {
      setSelectedOutputs((prevSet) => {
        const newSet = new Set(prevSet);
        newSet.add(data.output);
        return [...newSet];
      });
      setGateTypeOperationType(data["operation_type"]);
    }
  }, [ready]);

  /////////////////////////////////////////

  return (
    <form onSubmit={handleSubmit}>
      <h1 className="text-center mt-4">Specifications</h1>
      <div className="row">
        <div className="col">
          <div className="input-group input-group-md mb-3">
            <span className="input-group-text" id="inputGroup-sizing-sm">
              Model Name
            </span>
            <input
              type="text"
              className="form-control"
              value={modelName}
              onChange={handleModelNameChange}
            />
          </div>
        </div>
        <div className="col">
          <div className="input-group mb-3">
            <label className="input-group-text" htmlFor="circuit_type">
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
            <label className="input-group-text" htmlFor="gate_operation_type">
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
