<script>
    import { onMount } from 'svelte';
    import CreateProjectModal from './CreateProjectModal.svelte';
  
    let myProjects = [];
    let filteredMyProjects = [];
    let sharedProjects = [];
    let filteredSharedProjects = [];
    let showCreateModal = false;
    let error = null;
    let searchQuery = '';
    let statusFilter = 'All';
  
    // Fetch projects on mount
    onMount(async () => {
      await fetchProjects();
    });
  
    async function fetchProjects() {
      try {
        const response = await fetch('http://localhost:8000/');
        if (!response.ok) {
          throw new Error(`Failed to fetch projects: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data);
        myProjects = data.my_projects || [];
        sharedProjects = data.shared_projects || [];
        applyFilters();
      } catch (err) {
        error = 'Failed to load projects: ' + err.message;
        console.error('Fetch error:', err);
      }
    }
  
    // Apply search and filter
    function applyFilters() {
      let filtered = myProjects;
      if (searchQuery) {
        filtered = filtered.filter(project =>
          project.name.toLowerCase().includes(searchQuery.toLowerCase())
        );
      }
      if (statusFilter !== 'All') {
        filtered = filtered.filter(project => project.Status === statusFilter);
      }
      filteredMyProjects = filtered;
  
      filtered = sharedProjects;
      if (searchQuery) {
        filtered = filtered.filter(project =>
          project.name.toLowerCase().includes(searchQuery.toLowerCase())
        );
      }
      if (statusFilter !== 'All') {
        filtered = filtered.filter(project => project.Status === statusFilter);
      }
      filteredSharedProjects = filtered;
    }
  
    // Watch for changes in search and filter
    $: searchQuery, statusFilter, applyFilters();
  
    async function lockProject(projectName) {
      try {
        const response = await fetch(`http://localhost:8000/lock/${projectName}`, {
          method: 'POST'
        });
        if (response.ok) {
          myProjects = myProjects.map(project =>
            project.name === projectName ? { ...project, locked: true, Status: 'Inactive' } : project
          );
          applyFilters();
        } else {
          throw new Error('Failed to lock project');
        }
      } catch (err) {
        error = err.message;
      }
    }
  
    async function restoreProject(projectName) {
      try {
        const response = await fetch(`http://localhost:8000/restore/${projectName}`, {
          method: 'POST'
        });
        if (response.ok) {
          myProjects = myProjects.map(project =>
            project.name === projectName ? { ...project, locked: false, Status: 'Active' } : project
          );
          applyFilters();
        } else {
          throw new Error('Failed to restore project');
        }
      } catch (err) {
        error = err.message;
      }
    }
  
    // Placeholder for Run Scan
    function runScan(projectName) {
      console.log(`Running scan for project: ${projectName}`);
      // Implement API call if needed
    }
  </script>
  
  {#if error}
    <div class="alert alert-danger">{error}</div>
  {/if}
  
  <!-- Header with Title and Buttons -->
  <div class="d-flex justify-content-between align-items-center mt-4">
    <h1>Project Selection</h1>
    <div class="d-flex gap-2">
      <button class="btn btn-outline-secondary">
        <span class="import-icon">🖴</span> Import
      </button>
      <button class="btn create-btn text-white" on:click={() => (showCreateModal = true)}>
        + Create New
      </button>
    </div>
  </div>
  
  <!-- Recent Projects -->
  <h2 class="mt-4">Recent Projects</h2>
  <div class="row">
    {#each myProjects.slice(0, 3) as project}
      <div class="col-md-4 mb-3">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{project.name}</h5>
            <p class="card-text">
              Last Edit: {project.last_edit_date || project.Stamp_Date || 'N/A'}
            </p>
          </div>
          <div class="card-footer {project.Status === 'Active' ? 'border-success' : project.Status === 'Error' ? 'border-danger' : 'border-secondary'}">
            <small>Status: {project.Status}</small>
          </div>
        </div>
      </div>
    {/each}
    {#if myProjects.length === 0}
      <p>No recent projects available.</p>
    {/if}
  </div>
  
  <!-- All Projects -->
  <h2 class="mt-4">All Projects</h2>
  
  <!-- Search and Filter Bar -->
  <div class="d-flex justify-content-end mb-3">
    <div class="input-group w-50">
      <input
        type="text"
        class="form-control"
        placeholder="Search projects..."
        bind:value={searchQuery}
      />
      <select class="form-select" bind:value={statusFilter}>
        <option>All</option>
        <option>Active</option>
        <option>Error</option>
        <option>Inactive</option>
      </select>
    </div>
  </div>
  
  <!-- Tabs -->
  <ul class="nav nav-tabs mt-4" id="projectTabs" role="tablist">
    <li class="nav-item" role="presentation">
      <button
        class="nav-link active"
        id="my-projects-tab"
        data-bs-toggle="tab"
        data-bs-target="#my-projects"
        type="button"
        role="tab"
        aria-controls="my-projects"
        aria-selected="true"
      >
        My Projects
      </button>
    </li>
    <li class="nav-item" role="presentation">
      <button
        class="nav-link"
        id="shared-projects-tab"
        data-bs-toggle="tab"
        data-bs-target="#shared-projects"
        type="button"
        role="tab"
        aria-controls="shared-projects"
        aria-selected="false"
      >
        Shared Projects
      </button>
    </li>
  </ul>
  
  <div class="tab-content mt-3" id="projectTabsContent">
    <!-- My Projects Tab -->
    <div class="tab-pane fade show active" id="my-projects" role="tabpanel" aria-labelledby="my-projects-tab">
      {#if filteredMyProjects.length > 0}
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Project Name</th>
              <th>Last Edit</th>
              <th>Lead Analyst</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {#each filteredMyProjects as project}
              <tr data-project-name={project.name}>
                <td>{project.name}</td>
                <td>{project.last_edit_date || project.Stamp_Date || 'N/A'}</td>
                <td>{project.lead_analyst_initials || 'N/A'}</td>
                <td>
                  <span
                    class="badge {project.Status === 'Active'
                      ? 'bg-success'
                      : project.Status === 'Error'
                      ? 'bg-danger'
                      : 'bg-secondary'}"
                  >
                    {project.Status}
                  </span>
                </td>
                <td class="d-flex gap-2 align-items-center">
                  <button
                    class="btn btn-sm btn-primary"
                    disabled={project.Status !== 'Active'}
                    on:click={() => runScan(project.name)}
                  >
                    Run Scan
                  </button>
                  <div class="dropdown">
                    <button
                      class="btn btn-sm btn-outline-secondary"
                      type="button"
                      id="dropdownMenuButton-{project.name}"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      ⋮
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton-{project.name}">
                      {#if project.locked}
                        <li>
                          <button
                            class="dropdown-item"
                            on:click={() => restoreProject(project.name)}
                          >
                            Restore
                          </button>
                        </li>
                      {:else}
                        <li>
                          <button
                            class="dropdown-item"
                            on:click={() => lockProject(project.name)}
                          >
                            Lock
                          </button>
                        </li>
                      {/if}
                    </ul>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      {:else}
        <p>No projects match your criteria.</p>
      {/if}
    </div>
  
    <!-- Shared Projects Tab -->
    <div class="tab-pane fade" id="shared-projects" role="tabpanel" aria-labelledby="shared-projects-tab">
      {#if filteredSharedProjects.length > 0}
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Project Name</th>
              <th>Last Edit</th>
              <th>Lead Analyst</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {#each filteredSharedProjects as project}
              <tr>
                <td>{project.name}</td>
                <td>{project.last_edit_date || project.Stamp_Date || 'N/A'}</td>
                <td>{project.lead_analyst_initials || 'N/A'}</td>
                <td>
                  <span
                    class="badge {project.Status === 'Active'
                      ? 'bg-success'
                      : project.Status === 'Error'
                      ? 'bg-danger'
                      : 'bg-secondary'}"
                  >
                    {project.Status}
                  </span>
                </td>
                <td>
                  <button
                    class="btn btn-sm btn-primary"
                    disabled={project.Status !== 'Active'}
                    on:click={() => runScan(project.name)}
                  >
                    Run Scan
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      {:else}
        <p>No shared projects match your criteria.</p>
      {/if}
    </div>
  </div>
  
  {#if showCreateModal}
    <CreateProjectModal
      on:close={() => (showCreateModal = false)}
      on:projectCreated={() => {
        showCreateModal = false;
        fetchProjects();
      }}
    />
  {/if}
  
  <style>
    .create-btn {
      background-color: #007bff;
    }
    .import-icon {
      font-size: 1.2rem;
      margin-right: 0.5rem;
    }
    .card-footer {
      background-color: transparent;
    }
    .badge {
      font-size: 0.9rem;
    }
  </style>