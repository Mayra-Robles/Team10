<script>
    export let name = "Daniel Quijano";
    export let title = "Database";
    export let email = "dquijano@miners.utep.edu";
    export let phone = "+1 915 8456112";
    export let name1 = "Mayra Robles";
    export let title1 = "Front End";
    export let email1 = "mlrobles@miners.utep.edu";
    export let phone1 = "+1 915 8456112";

    
  </script>
  
  <div class="min-h-screen flex items-center justify-center bg-gray-100 p-4">
    <div class="bg-white rounded-2xl shadow-lg p-6 max-w-sm w-full text-center space-y-4">
      <h1 class="text-2xl font-bold text-gray-800">{name}</h1>
      <p class="text-sm text-gray-600">{title}</p>
  
      <div class="text-left mt-4 space-y-2">
        <p><strong>📧 Mail:</strong> <a href={`mailto:${email}`} class="text-blue-600 hover:underline">{email}</a></p>
        <p><strong>📞 Phone:</strong> {phone}</p>
      </div>
      <h1 class="text-2xl font-bold text-gray-800">{name1}</h1>
      <p class="text-sm text-gray-600">{title1}</p>
      <div class="text-left mt-4 space-y-2">
        <p><strong>📧 Mail:</strong> <a href={`mailto:${email1}`} class="text-blue-600 hover:underline">{email1}</a></p>
        <p><strong>📞 Phone:</strong> {phone1}</p>
      </div>
    </div>
  </div>
  