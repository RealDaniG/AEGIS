// Test script to verify Hebrew Quantum Field visualization is working
console.log("Testing Hebrew Quantum Field Visualization...");

// Check if the required functions exist
const requiredFunctions = [
    'initHebrewQuantumField',
    'animateHebrewField',
    'drawHebrewField',
    'updateHebrewField',
    'toggleHebrewField',
    'resetHebrewField'
];

console.log("Checking for required Hebrew Quantum Field functions...");
let allFunctionsFound = true;

for (const func of requiredFunctions) {
    if (typeof window[func] === 'function') {
        console.log(`✅ ${func} function found`);
    } else {
        console.log(`❌ ${func} function NOT found`);
        allFunctionsFound = false;
    }
}

// Check if the canvas element exists
console.log("Checking for Hebrew Quantum Field canvas element...");
const canvas = document.getElementById('hebrew-quantum-canvas');
if (canvas) {
    console.log("✅ Hebrew Quantum Field canvas found");
} else {
    console.log("❌ Hebrew Quantum Field canvas NOT found");
    allFunctionsFound = false;
}

// Check if the panel exists
console.log("Checking for Hebrew Quantum Field panel...");
const panel = document.querySelector('.hebrew-visualization-panel');
if (panel) {
    console.log("✅ Hebrew Quantum Field panel found");
} else {
    console.log("❌ Hebrew Quantum Field panel NOT found");
    allFunctionsFound = false;
}

// Test initialization
if (allFunctionsFound) {
    console.log("Testing Hebrew Quantum Field initialization...");
    try {
        // Initialize the Hebrew Quantum Field
        initHebrewQuantumField();
        console.log("✅ Hebrew Quantum Field initialized successfully");
        
        // Test toggle function
        toggleHebrewField();
        console.log("✅ Hebrew Quantum Field toggle function works");
        
        // Test reset function
        resetHebrewField();
        console.log("✅ Hebrew Quantum Field reset function works");
        
        console.log("🎉 ALL HEBREW QUANTUM FIELD TESTS PASSED!");
    } catch (error) {
        console.log(`❌ Error testing Hebrew Quantum Field: ${error.message}`);
        allFunctionsFound = false;
    }
} else {
    console.log("❌ MISSING REQUIRED HEBREW QUANTUM FIELD COMPONENTS");
}

console.log("Hebrew Quantum Field Visualization Test Complete");