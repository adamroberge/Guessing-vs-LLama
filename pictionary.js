// pictionary.js

// Canvas setup
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;

// Set up canvas for drawing
ctx.lineWidth = 5;
ctx.lineCap = 'round';
ctx.strokeStyle = '#000';

// Drawing functions
function startDrawing(e) {
	e.preventDefault();
	isDrawing = true;
	draw(e);
}

function stopDrawing() {
	isDrawing = false;
	ctx.beginPath();
}

function getPosition(e) {
	let x, y;
	if (e.type.startsWith('touch')) {
		const rect = canvas.getBoundingClientRect();
		x = e.touches[0].clientX - rect.left;
		y = e.touches[0].clientY - rect.top;
	} else {
		x = e.offsetX;
		y = e.offsetY;
	}
	return { x, y };
}

function draw(e) {
	if (!isDrawing) return;
	e.preventDefault();

	const { x, y } = getPosition(e);

	ctx.lineTo(x, y);
	ctx.stroke();
	ctx.beginPath();
	ctx.moveTo(x, y);
}

// Event listeners for drawing
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('touchstart', startDrawing, { passive: false });
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('touchmove', draw, { passive: false });
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('touchend', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// Clear canvas
document.getElementById('clearButton').addEventListener('click', () => {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// Set up the API URL
const API_URL = 'http://127.0.0.1:5001'; // Update if necessary


// Start new game
document.getElementById('startButton').addEventListener('click', async () => {
	try {
		const response = await fetch(`${API_URL}/begin_pictionary`, {
			method: 'GET',
			mode: 'cors'
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const data = await response.json();
		document.getElementById('topic').textContent = `Draw: ${data.topic}`;
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		document.getElementById('result').textContent = '';
		document.getElementById('result').className = '';
	} catch (error) {
		console.error(`Failed to start new game:`, error);
		document.getElementById('topic').textContent = `Error: ${error.message}`;
	}
});

// Predict drawing
document.getElementById('predictButton').addEventListener('click', async () => {
	const resultDiv = document.getElementById('result');
	resultDiv.textContent = 'Processing...';
	resultDiv.className = '';

	try {
		// Create a temporary canvas to add white background
		const tempCanvas = document.createElement('canvas');
		tempCanvas.width = canvas.width;
		tempCanvas.height = canvas.height;
		const tempCtx = tempCanvas.getContext('2d');

		// Fill with white background
		tempCtx.fillStyle = 'white';
		tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

		// Draw the original canvas content on top
		tempCtx.drawImage(canvas, 0, 0);

		// Generate base64 image string from the temporary canvas
		const base64Image = tempCanvas.toDataURL('image/png').split(',')[1];

		const formData = new FormData();
		formData.append('image', base64Image);

		const response = await fetch(`${API_URL}/describe_image`, {
			method: 'POST',
			body: formData,
			mode: 'cors'
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const data = await response.json();
		console.log(data);

		resultDiv.textContent = `Prediction: ${data.description}`;
		if (data.correct) {
			resultDiv.className = 'success';
			resultDiv.textContent += '\nYou drew it correctly!';
		} else {
			resultDiv.className = 'failure';
			resultDiv.textContent += '\nTry again!';
		}
	} catch (error) {
		console.error(`Attempt failed:`, error);
		resultDiv.textContent = `Error: ${error.message}`;
	}
});
