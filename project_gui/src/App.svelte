<script>
    import { onMount } from 'svelte';
    import axios from 'axios';

    let projects = [];
    let newProject = { name: '', date: '', time: '' };

    onMount(async () => {
        try {
            const response = await axios.get('http://localhost:5000/my_projects/MR');
            projects = [...response.data];
        } catch (error) {
            console.error("Error fetching projects:", error);
        }
    });

    async function createProject() {
        const data = new URLSearchParams();
        data.append("project_name", newProject.name);
        data.append("start_date", newProject.date);
        data.append("time", newProject.time);
        data.append("lead_analyst_initials", "MR");
        data.append("description", "");

        try {
            await axios.post('http://localhost:5000/create', data);
            const response = await axios.get('http://localhost:5000/my_projects/MR');
            projects = [...response.data];
            newProject = { name: '', date: '', time: '' };
        } catch (error) {
            console.error("Error creating project:", error);
        }
    }

    async function deleteProject(projectName) {
        try {
            await axios.post(`http://localhost:5000/delete/${projectName}`);
            const response = await axios.get('http://localhost:5000/my_projects/MR');
            projects = [...response.data];
        } catch (error) {
            console.error("Error deleting project:", error);
        }
    }
</script>

<h1>Project Management</h1>
<div>
    <h2>My Projects</h2>
    <ul>
        {#each projects as project}
            <li>{project.project_name} - {project.status}
                <button on:click={() => deleteProject(project.project_name)}>Delete</button>
            </li>
        {/each}
    </ul>

    <h3>Create Project</h3>
    <input bind:value={newProject.name} placeholder="Name" />
    <input bind:value={newProject.date} placeholder="YYYY-MM-DD" />
    <input bind:value={newProject.time} placeholder="HH:MM" />
    <button on:click={createProject}>Create</button>
</div>
