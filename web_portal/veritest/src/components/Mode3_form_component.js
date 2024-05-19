"use client";
import { useState } from "react";

const DropdownFormControl = () => {
  const initialOptions = ["Option 1", "Option 2", "Option 3"];
  const [options, setOptions] = useState(initialOptions);
  const [selectedItems, setSelectedItems] = useState([]);

  const handleSelect = (e) => {
    const option = e.target.value;
    if (option) {
      setOptions(options.filter((opt) => opt !== option));
      setSelectedItems([...selectedItems, option]);
    }
    e.target.value = ""; // Reset the dropdown selection
  };

  const handleRemove = (option) => {
    setSelectedItems(selectedItems.filter((item) => item !== option));
    setOptions([...options, option]);
  };

  return (
    <div className="container mt-4">
      <div className="mb-3">
        <label htmlFor="dropdown" className="form-label">
          Select an Option
        </label>
        <select
          id="dropdown"
          className="form-select"
          onChange={handleSelect}
          value=""
        >
          <option value="" disabled>
            Select an option
          </option>
          {options.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>
      <ul className="list-group">
        {selectedItems.map((item, index) => (
          <li
            key={index}
            className="list-group-item d-flex justify-content-between align-items-center"
          >
            {item}
            <button
              type="button"
              className="btn btn-outline-danger btn-sm"
              onClick={() => handleRemove(item)}
            >
              &times;
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DropdownFormControl;
