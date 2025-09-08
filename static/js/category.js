async function addLink(event, categoryId) {
  event.preventDefault();

  const label = document.getElementById("label").value;
  const url = document.getElementById("url").value;

  await fetch("/api/add_link", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      category_id: parseInt(categoryId), 
      label: label,
      url: url
    })
  });

  location.reload();
}
