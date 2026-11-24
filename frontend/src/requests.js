const apiBase = "http://localhost:5000/";

export const health = async () => {
  const endpoint = "health";
  const response = await fetch(apiBase + endpoint);
  const data = await response.json();
  console.log("health", data);
  return data;
};
