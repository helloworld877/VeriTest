"use client";
import React from "react";

const DropdownFormControl = ({
  label,
  options,
  selectedItems,
  onSelect,
  onRemove,
}) => {
  const handleSelect = (e) => {
    const option = e.target.value;
    if (option) {
      onSelect(option);
    }
    e.target.value = ""; // Reset the dropdown selection
  };

  return (
    <div className="mb-3">
      <label htmlFor={label} className="form-label">
        <h2>{label}</h2>
      </label>
      <select
        id={label}
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
      <ul className="list-group mt-3">
        {selectedItems.map((item, index) => (
          <li
            key={index}
            className="list-group-item d-flex justify-content-between align-items-center"
          >
            {item}
            <button
              type="button"
              className="btn btn-outline-danger btn-sm"
              onClick={() => onRemove(item)}
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
