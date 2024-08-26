// Declare the chart dimensions and margins.
const width = 1000;
const height = 400;
const marginTop = 20;
const marginRight = 20;
const marginBottom = 30;
const marginLeft = 40;

// Declare the x (horizontal position) scale.
const x = d3
  .scaleLinear()
  .domain([0, 12000]) // Set the x-axis domain from 0 to 12000
  .range([marginLeft, width - marginRight]);

// Declare the y (vertical position) scale.
const y = d3
  .scaleLinear()
  .domain([-20, 0]) // Set the y-axis domain from -20 to 0
  .range([height - marginBottom, marginTop]);

// Create the SVG container.
const svg = d3.create("svg").attr("width", width).attr("height", height);
document.getElementById("container").appendChild(svg.node());

// Add the x-axis.
svg
  .append("g")
  .attr("transform", `translate(0,${height - marginBottom})`)
  .call(d3.axisBottom(x));

// Add the y-axis.
svg
  .append("g")
  .attr("transform", `translate(${marginLeft},0)`)
  .call(d3.axisLeft(y));

const getData = async () => {
  try {
    const response = await fetch("../api/outputs/20240826_145912.json");
    const data = await response.json();

    // Log the data to check its structure
    console.log("Data loaded:", data);

    // // Define and log time markers
    // const timeMarkers = [1000, 2300, 4000, 7000, 10000];
    // console.log("Time Markers:", timeMarkers);

    // Plot the lines
    svg
      .selectAll("line.time-marker")
      .data(data.grid)
      .enter()
      .append("line")
      .attr("class", "time-marker")
      .attr("x1", (d) => x(d))
      .attr("x2", (d) => x(d))
      .attr("y1", height - marginBottom) // Bottom of the chart
      .attr("y2", marginTop) // Top of the chart
      .attr("stroke", "gray")
      .attr("stroke-width", 0.5)
      .attr("stroke-dasharray", "4,4"); // Optional: makes the line dashed

    // Plot the circles
    svg
      .selectAll("circle")
      .data(data.points)
      .enter()
      .append("circle")
      .attr("cx", (d) => x(d.time)) // Use 'time' for the x position
      .attr("cy", (d) => y(d.amplitude)) // Use 'amplitude' for the y position
      .attr("r", 1.5) // Radius of the circle
      .attr("fill", "steelblue"); // Circle color

    // Append the SVG element to the container
    const container = document.getElementById("container");
    container.append(svg.node());
  } catch (error) {
    console.error("Error loading data:", error);
  }
};

getData();
