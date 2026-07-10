// Update CIBIL score label live as slider moves
const cibilSlider = document.getElementById('cibil_score');
const cibilValue = document.getElementById('cibilValue');
cibilSlider.addEventListener('input', () => {
  cibilValue.textContent = cibilSlider.value;
});

// Grab state boxes
const placeholderState = document.getElementById('placeholderState');
const loadingState = document.getElementById('loadingState');
const resultState = document.getElementById('resultState');
const errorState = document.getElementById('errorState');

function showState(state) {
  placeholderState.classList.add('hidden');
  loadingState.classList.add('hidden');
  resultState.classList.add('hidden');
  errorState.classList.add('hidden');
  state.classList.remove('hidden');
}

// Handle form submit
document.getElementById('loanForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  showState(loadingState);

  // Collect form data with keys matching app.py exactly
  const payload = {
    dependents: document.getElementById('dependents').value,
    education: document.getElementById('education').value,
    self_employed: document.getElementById('self_employed').value,
    income: document.getElementById('income').value,
    loan_amount: document.getElementById('loan_amount').value,
    loan_term: document.getElementById('loan_term').value,
    cibil_score: document.getElementById('cibil_score').value,
    residential_assets: document.getElementById('residential_assets').value,
    commercial_assets: document.getElementById('commercial_assets').value,
    luxury_assets: document.getElementById('luxury_assets').value,
    bank_assets: document.getElementById('bank_assets').value
  };

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      throw new Error(data.error || 'Prediction failed');
    }

    displayResult(data);

  } catch (err) {
    document.getElementById('errorMsg').textContent = err.message;
    showState(errorState);
  }
});

function displayResult(data) {
  const resultTitle = document.getElementById('resultTitle');
  const resultIcon = document.getElementById('resultIcon');
  const probBarFill = document.getElementById('probBarFill');
  const probValue = document.getElementById('probValue');

  resultState.classList.remove('approved', 'rejected');

  if (data.approved) {
    resultState.classList.add('approved');
    resultIcon.textContent = '✅';
    resultTitle.textContent = 'Loan Approved!';
    probValue.textContent = data.approval_probability.toFixed(1);
    probBarFill.style.width = data.approval_probability + '%';
  } else {
    resultState.classList.add('rejected');
    resultIcon.textContent = '❌';
    resultTitle.textContent = 'Loan Rejected';
    probValue.textContent = data.rejection_probability.toFixed(1);
    probBarFill.style.width = data.rejection_probability + '%';
  }

  showState(resultState);
}

// Reset back to the form / placeholder view
function resetForm() {
  document.getElementById('loanForm').reset();
  cibilValue.textContent = cibilSlider.value;
  showState(placeholderState);
}