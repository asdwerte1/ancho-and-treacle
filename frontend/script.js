document.addEventListener("DOMContentLoaded", async () => {
  const galleryGrid = document.getElementById("gallery-grid");

  const yearElement = document.getElementById("year");
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }

  await getPhotos(galleryGrid, 0);

  document.getElementById("load-more").addEventListener("click", async () => {
    const numberOfPhotos = document
      .getElementById("gallery-grid")
      .querySelectorAll("img").length;
    await getPhotos(galleryGrid, numberOfPhotos);
  });
});

async function getPhotos(gridElement, numberOfPhotos = 0) {
  if (!gridElement) return;

  let response;

  try {
    if (numberOfPhotos == 0) {
      response = await fetch("/api/photos");
    } else {
      response = await fetch(`/api/photos?number=${numberOfPhotos}`);
    }

    if (!response.ok) {
      throw new Error("API response was not successful");
    }

    const photos = await response.json();

    if (numberOfPhotos === 0) {
      gridElement.innerHTML = "";
    }

    photos.forEach((photo) => {
      const card = document.createElement("article");
      card.className = "col photo-card";

      const cleanDate = new Date(photo.date).toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });

      card.innerHTML = `
                    <div class="photo-card-inner">
                      <figure class="m-0 p-0 d-flex flex-column h-100">
                      <div class="img-wrapper">
                          <img  src="/images/${photo.name}"
                                alt="Ancho and Treacle Capture"
                                class="img-fluid rounded object-fit-cover flex-grow-1 opacity-0 transition-fade"
                                loading="lazy"
                                onload="this.classList.remove('opacity-0')">
                        </div>
                        <figcaption class="pt-2 text-start small">
                          Captured: <span class="highlight-date">${cleanDate}</span>
                        </figcaption>
                      </figure>
                    </div>`;

      galleryGrid.appendChild(card);
    });
  } catch (error) {
    console.error("Error fetching images.", error);
  }
}
