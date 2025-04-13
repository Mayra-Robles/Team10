<script>
    import { onMount } from 'svelte';
  
    let folders = [];
    let error = null;
  
    onMount(async () => {
      await fetchFolders();
    });
  
    async function fetchFolders() {
      try {
        const response = await fetch('http://localhost:9000/folders');
        if (!response.ok) {
          throw new Error(`Failed to fetch folders: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        folders = data.my_folders || [];
      } catch (err) {
        error = 'Failed to load folders: ' + err.message;
        console.error('Fetch error:', err);
      }
    }
  </script>
  
  {#if error}
    <div class="alert alert-danger">{error}</div>
  {/if}
  
  <!-- Header -->
  <div class="d-flex justify-content-between align-items-center mt-4">
    <h1>Project Folders</h1>
    <button class="btn create-btn text-white">
      + Create Folder
    </button>
  </div>
  
  <!-- Folder Cards -->
  <h2 class="mt-4">Your Folders</h2>
  <div class="row">
    {#each folders as folder}
      <div class="col-md-4 mb-3">
        <div class="card h-100 clickable-card">
          <div class="card-body">
            <h5 class="card-title">{folder.path}</h5>
            <p class="card-text">
              Created on: {folder.created_at?.slice(0, 10) || 'Unknown'}
            </p>
          </div>
        </div>
      </div>
    {/each}
    {#if folders.length === 0}
      <p>No folders found.</p>
    {/if}
  </div>
  
  <style>
    .create-btn {
      background-color: #007bff;
    }
    .create-btn:hover{
        background-color: #000000;
    }
    .clickable-card {
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .clickable-card:hover {
        background-color: #0000004e;
    }
    
  </style>
  