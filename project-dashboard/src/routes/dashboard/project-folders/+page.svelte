<script>
  import { onMount } from 'svelte';

  let folders = [];
  let recentFolders = [];
  let otherFolders = [];
  let error = null;
  

  onMount(async () => {
    await fetchFolders();
  });

  async function fetchFolders() {
    try {
      const response = await fetch('http://localhost:9000/folders/');
      if (!response.ok) {
        throw new Error(`Failed to fetch folders: ${response.status} ${response.statusText}`);
      }
      const data = await response.json();
      folders = data.my_folders || [];
      const folders_sorted= [...folders];

      // Ordenar por fecha y separar recientes
      folders_sorted.sort((a, b) => {
      const dateA = Date.parse(a.creation_date); 
      const dateB =  Date.parse(b.creation_date);  
      return dateB - dateA;  
    });
      recentFolders = folders_sorted.slice(0, 3);
      otherFolders = folders;
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

<!-- Recent Folders -->
{#if recentFolders.length > 0}
  <h2 class="mt-4">Recent Folders</h2>
  <div class="row">
    {#each recentFolders as folder}
      <div class="col-md-4 mb-3">
        <div class="card h-100 clickable-card">
          <div class="card-body">
            <h5 class="card-title">{folder.path}</h5>
            <p class="card-text">
              Created on: {folder.creation_date?.slice(0, 19) || 'Unknown'}
            </p>
          </div>
        </div>
      </div>
    {/each}
  </div>
{/if}

<!-- All Other Folders -->
<h2 class="mt-4">Your Folders</h2>
<div class="row">
  {#each otherFolders as folder}
    <div class="col-md-3 mb-3">
      <div class="card h-100 clickable-card">
        <div class="card-body">
          <h5 class="card-title">{folder.path}</h5>
          <p class="card-text">
            Created on: {folder.creation_date?.slice(0, 19) || 'Unknown'}
          </p>
        </div>
      </div>
    </div>
  {/each}
  {#if otherFolders.length === 0}
    <p>No folders found.</p>
  {/if}
</div>

<style>
  .create-btn {
    background-color: #007bff;
  }
  .create-btn:hover {
    background-color: #000000;
  }
  .clickable-card {
    cursor: pointer;
    transition: background-color 0.2s;
  }
  .clickable-card:hover {
    background-color: #0000004e;
  }
  .recent-card {
    border: 2px solid #007bff;
  }
</style>
