<script>
  import { onMount } from 'svelte';
  let fileInput;
  let canvas;
  let onLoading = false;
  let alertInfo = {
    show: false,
    message: '',
  };
  let alertError = {
    show: false,
    message: '',
  };

  onMount(() => {
    fileInput.addEventListener('change', (e) => {
      onLoading = true;
      alertInfo.show = false;
      alertError.show = false;
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.src = e.target.result;
        img.onload = () => {
          // const canvas = document.getElementById('preview-image');
          const ctx = canvas.getContext('2d');

          // Clear canvas
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // set canvas width to 100% (resize according to container)
          // canvas.width = canvas?.clientWidth;
          
          // calculate aspect ratio and set height according to aspect ratio
          const aspectRatio = img.width / img.height;
          const newHeight = canvas.width / aspectRatio;
          canvas.height = newHeight;
          ctx.drawImage(img, 0, 0, canvas.width, newHeight);

          const data = canvas.toDataURL('image/jpeg');
          // https://universe.roboflow.com/penulisanilmiah-11njc/organic-and-anorganic-waste
          fetch('https://detect.roboflow.com/organic-and-anorganic-waste/3?' + new URLSearchParams({
            api_key: 'SJWUY5OVPN5x9oYgOQpv'
          }), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: data,
          })
            .then((res) => res.json())
            .then((data) => {
              onLoading = false;
              alertInfo.show = true;
              if (data.predictions.length === 0) {
                alertInfo.message = 'No waste detected';
              } else {
                // ctx.strokeStyle = 'green';
                ctx.lineWidth = 3;
                alertInfo.message = `<h3>Waste Detected</h3><ul>`;
                for (var i = 0; i < data.predictions.length; i++) {
                  var classify = data.predictions[i].class
                  var confidence = data.predictions[i].confidence;
                  var type = 'organic';
                  if (classify.search(/anorganik/i) >= 0) {
                    type = 'anorganic';
                  }
                  alertInfo.message += `<li>${classify} [${type}] </li>`;

                  // draw rectangle
                  ctx.strokeStyle = type === 'organic' ? 'green' : 'red';
                  var startX = data.predictions[i].x - data.predictions[i].width / 2;
                  var startY = data.predictions[i].y - data.predictions[i].height / 2;
                  ctx.strokeRect(startX, startY, data.predictions[i].width, data.predictions[i].height);

                  // draw label with background
                  ctx.fillStyle = type === 'organic' ? 'green' : 'red';
                  ctx.fillRect(startX, startY - 20, ctx.measureText(`${classify} (${(confidence * 100).toFixed(2)}%)`).width + 10, 20);
                  ctx.fillStyle = 'white';
                  ctx.fillText(`${classify} (${(confidence * 100).toFixed(2)}%)`, startX, startY - 5);
                  
                }
                alertInfo.message += `</ul>`;
              }
              console.log(data);
            })
            .catch((err) => {
              onLoading = false;
              alertError.show = true;
              alertError.message = 'Error occurred while processing image';
              console.error(err);
            });
        };
      };
      reader.readAsDataURL(file);
    });
  });
</script>

<!-- loading spinner container -->
{#if onLoading}
  <div class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50" >
    <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500">
    </div>
  </div>
{/if}

<div class="navbar bg-primary text-primary-content">
  <button class="btn btn-ghost text-xl">WasteAI</button>
</div>
<div class="container mx-auto mt-2 px-4">
  <div class="text-center mb-4">
    <div class="w-full mb-16">
      <h1 class="text-3xl font-bold">Waste Detection</h1>
      <p class="py-6">
        Provident cupiditate voluptatem et in. Quaerat fugiat ut assumenda excepturi exercitationem
        quasi.
      </p>
      <input type="file" id="image-upload" bind:this={fileInput} class="file-input file-input-bordered w-full max-w-xs" />
      <!-- show image -->
      <div class="my-4 w-full">
        <canvas bind:this={canvas} class="w-full"></canvas>
      </div>
      {#if alertInfo.show }
      <div role="alert" class="alert alert-info">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          class="h-6 w-6 shrink-0 stroke-current">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <!-- show alertInfo.message -->
        <span>{@html alertInfo.message}</span>
      </div>
      {/if}
      {#if alertError.show }
      <div role="alert" class="alert alert-error">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 shrink-0 stroke-current"
          fill="none"
          viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{@html alertError.message}</span>
      </div>
      {/if}
    </div>
  </div>
</div>
<div class="btm-nav">
  <button>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
    </svg>
  </button>
  <button class="active">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  </button>
  <button>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  </button>
</div>