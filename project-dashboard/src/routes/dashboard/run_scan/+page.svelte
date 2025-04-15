<script>
    function gotoCrawler() {
      window.location.href = "/main/tools/Crawler";
    }
    function gotoFuzzer() {
      window.location.href = "/main/tools/Fuzzer";
    }
    function gotoBruteForcer() {
      window.location.href = "/main/tools/BruteForcer";
    }
    function gotoAI() {
      window.location.href = "/main/tools/AI";
    }
  </script>
  
  <div class="container mt-5">
    <div class="d-flex flex-column align-items-start mb-4">
      <h1 class="mb-1">Tools</h1>
      <p class="subtitle">Base Perimeter Network</p>
    </div>
  
    <div class="row">
      <div class="col-12 mb-4">
        <div class="card h-100 clickable-card">
          <div class="card-body d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Crawler</h5>
            <button class="btn btn-sm btn-primary" on:click={gotoCrawler}>Select</button>
          </div>
        </div>
      </div>
      <div class="col-12 mb-4">
        <div class="card h-100 clickable-card">
          <div class="card-body d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Fuzzer</h5>
            <button class="btn btn-sm btn-primary" on:click={gotoFuzzer}>Select</button>
          </div>
        </div>
      </div>
      <div class="col-12 mb-4">
        <div class="card h-100 clickable-card">
          <div class="card-body d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Brute Forcer</h5>
            <button class="btn btn-sm btn-primary" on:click={gotoBruteForcer}>Select</button>
          </div>
        </div>
      </div>
      <div class="col-12 mb-4">
        <div class="card h-100 clickable-card">
          <div class="card-body d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">AI Credential Generator</h5>
            <button class="btn btn-sm btn-primary" on:click={gotoAI}>Select</button>
          </div>
        </div>
      </div>
    </div>
    <div class="col-12 mb-4">
        <div class="card h-100 clickable-card">
          <div class="card-body d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">SQL injector</h5>
            <button class="btn btn-sm btn-primary" on:click={gotoAI}>Select</button>
          </div>
        </div>
      </div>
  </div>
  
  <style>
    h1 {
      font-size: 2rem;
      font-weight: 500;
      color: #333;
      margin: 0;
    }
  
    .subtitle {
      font-size: 1rem;
      font-weight: 400;
      color: #6c757d; /* Bootstrap's muted text color */
      margin: 0;
    }
  
    .card {
      border: none;
      border-radius: 0.5rem;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
  
    .card-body {
      padding: 1.5rem;
    }
  
    .card-title {
      font-size: 1.25rem;
      font-weight: 500;
      color: #495057;
    }
  
    .btn-primary {
      background-color: #007bff;
      border-color: #007bff;
      transition: background-color 0.2s ease;
    }
  
    .btn-primary:hover {
      background-color: #0056b3;
      border-color: #0056b3;
    }
  
    .clickable-card {
    background-color:#00000006;
      cursor: pointer;
      transition: background-color 0.2s ease;
    }
  
    .clickable-card:hover {
      background-color: #f8f9fa;
    }
  </style>