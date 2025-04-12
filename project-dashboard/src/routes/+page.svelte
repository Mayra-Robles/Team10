<script>
    import { onMount } from 'svelte';
    import CreateProjectModal from './CreateProjectModal.svelte';

    let myProjects = [];
    let sharedProjects = [];
    let showCreateModal = false;
    let error = null;

    onMount(async () => {
        try {
            const response = await fetch('http://localhost:9000/');
            if (!response.ok) {
                throw new Error(`Failed to fetch projects: ${response.status} ${response.statusText}`);
            }
            const data = await response.json();
            console.log('Fetched data:', data); // Debug: log the response
            myProjects = data.my_projects || [];
            sharedProjects = data.shared_projects || [];
        } catch (err) {
            error = 'Failed to load projects: ' + err.message;
            console.error('Fetch error:', err); // Debug: log the error
        }
    });

    async function lockProject(projectName, lead_analyst_initials) {
        try {
            const response = await fetch(`http://localhost:9000/lock/${projectName}/${lead_analyst_initials}`, {
                method: 'POST'
            });
            if (response.ok) {
                myProjects = myProjects.map(project =>
                    project.name === projectName ? { ...project, locked: true } : project
                
                );
            } else {
                throw new Error('Failed to lock project');
            }
        } catch (err) {
            error = err.message;
        }
    }

    async function unlockProject(projectName, lead_analyst_initials) {
        try {
            const response = await fetch(`http://localhost:9000/unlock/${projectName}/${lead_analyst_initials}`, {
                method: 'POST'
            });
            if (response.ok) {
                myProjects = myProjects.map(project =>
                    project.name === projectName ? { ...project, locked: false } : project
                );
            } else {
                throw new Error('Failed to unlock project');
            }
        } catch (err) {
            error = err.message;
        }
    }
</script>

<div class="container-fluid">
    <div class="row">
        <nav class="col-md-2 d-none d-md-block sidebar">
            <div class="position-sticky">
                <h4 class="text-center">Project Dashboard</h4>
                <ul class="nav flex-column">
                    <li class="nav-item"><a class="nav-link" href="#">📁</a></li>
                    <li class="nav-item"><a class="nav-link" href="#">📊</a></li>
                    <li class="nav-item"><a class="nav-link" href="#">🗑️</a></li>
                </ul>
            </div>
        </nav>

        <main class="col-md-10 ms-sm-auto px-md-4">
            {#if error}
                <div class="alert alert-danger">{error}</div>
            {/if}
            <div class="d-flex justify-content-between align-items-center mt-4">
                <h1>Project Selection</h1>
                <button class="btn create-btn text-white" on:click={() => (showCreateModal = true)}>
                    + Create New
                </button>
            </div>

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
                <!-- My Projects -->
                <div class="tab-pane fade show active" id="my-projects" role="tabpanel" aria-labelledby="my-projects-tab">
                    {#if myProjects.length > 0}
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Project Name</th>
                                    <th>Last Edit</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each myProjects as project}
                                    <tr data-project-name={project.name}>
                                        <td>{project.name}</td>
                                        <td>{project.last_edit_date || project.Stamp_Date || 'N/A'}</td>
                                        <td>{project.Status}</td>
                                        <td class="d-flex gap-2">
                                            <button class="btn btn-sm btn-primary">Join</button>
                                            {#if project.locked}
                                                <button
                                                    class="btn btn-sm btn-warning"
                                                    on:click={() => unlockProject(project.name)}
                                                >
                                                    Unlock
                                                </button>
                                            {:else}
                                                <button
                                                    class="btn btn-sm btn-secondary"
                                                    on:click={() => lockProject(project.name, project.lead_analyst_initials)}
                                                >
                                                    Lock
                                                </button>
                                            {/if}
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    {:else}
                        <p>No projects found.</p>
                    {/if}
                </div>

                <!-- Shared Projects -->
                <div class="tab-pane fade" id="shared-projects" role="tabpanel" aria-labelledby="shared-projects-tab">
                    {#if sharedProjects.length > 0}
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Project Name</th>
                                    <th>Last Edit</th>
                                    <th>Status</th>
                                    <th>ID</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each sharedProjects as project}
                                    <tr>
                                        <td>{project.name}</td>
                                        <td>{project.last_edit_date || project.Stamp_Date || 'N/A'}</td>
                                        <td>{project.Status || 'Unknown'}</td>
                                        <td>{project.name}</td>
                                        <td>
                                            <button class="btn btn-sm btn-primary">Join</button>
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    {:else}
                        <p>No shared projects found.</p>
                    {/if}
                </div>
            </div>
        </main>
    </div>
</div>

{#if showCreateModal}
    <CreateProjectModal
        on:close={() => (showCreateModal = false)}
        on:projectCreated={() => {
            showCreateModal = false;
            fetch('http://localhost:5000/')
                .then(res => res.json())
                .then(data => {
                    myProjects = data.my_projects || [];
                    sharedProjects = data.shared_projects || [];
                })
                .catch(err => {
                    error = 'Failed to refresh projects: ' + err.message;
                });
        }}
    />
{/if}