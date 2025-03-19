<script>
    import { onMount } from 'svelte';
    import axios from 'axios';

    let projects = [];
    let newProject = { name: '', date: '', time: '' };

    onMount(async () => {
        const response = await axios.get('http://localhost:5000/my_projects/MR');
        projects = response.data;
    });

    async function createProject() {
        await axios.post('http://localhost:5000/create', newProject);
        const response = await axios.get('http://localhost:5000/my_projects/MR');
        projects = response.data;
        newProject = { name: '', date: '', time: '' };
    }
</script>

<h1>Project Management</h1>
<div>
    <h2>My Projects</h2>
    <ul>
        {#each projects as project}
            <li>{project.project_name} - {project.status}</li>
        {/each}
    </ul>
    <h3>Create Project</h3>
    <input bind:value={newProject.name} placeholder="Name" />
    <input bind:value={newProject.date} placeholder="YYYY-MM-DD" />
    <input bind:value={newProject.time} placeholder="HH:MM" />
    <button on:click={createProject}>Create</button>
</div>