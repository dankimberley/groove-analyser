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
  .domain([-75, -5]) // Set the y-axis domain from -20 to 0
  .range([height - marginBottom, marginTop]);

const colourScale = d3.scaleLinear().domain([-15, -5]).range(["blue", "red"]);
const getColour = (value) => colourScale(value);

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

let grid = []

const getTimeDifference = (point, grid) => {
  let inputOnset = point.time
  let gridOnset = grid.grid.find(item => item.bar === point.bar && item.position === point.position).time;
  return inputOnset - gridOnset
}

const getData = async () => {
  try {
    const response = await fetch("../api/outputs/output.json");
    const data = await response.json();

    // Log the data to check its structure
    console.log("Data loaded:", data);
    grid = data.grid

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
      .attr("x1", (d) => x(d.time))
      .attr("x2", (d) => x(d.time))
      .attr("y1", height - marginBottom) // Bottom of the chart
      .attr("y2", marginTop) // Top of the chart
      .attr("stroke", (d) => (d.position === 0 ? "black" : "gray"))
      .attr("stroke-width", (d) => (d.position === 0 ? 1 : 0.5))
      .attr("stroke-dasharray", "4,4"); // Optional: makes the line dashed

    // waveform
    svg.append("path")
      .datum(data.amplitudes)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 0.4)
      .attr("d", d3.line()
        .curve(d3.curveCardinal)
        .x(function(d) { return x(d.time) })
        .y(function(d) { return y(d.amplitude) })
        )

    // Plot the circles
    svg
      .selectAll("circle")
      .data(data.points)
      .enter()
      .append("circle")
      .attr("cx", (d) => x(d.time)) // Use 'time' for the x position
      .attr("cy", (d) => y(d.amplitude)) // Use 'amplitude' for the y position
      .attr("r", (d) => (d.position === 0 ? 3 : 1.5)) // Radius of the circle
      .attr("fill", (d) => getColour(d.amplitude))
      .on("mouseover", function (event, d) {
        // Enlarge the circle on hover
        d3.select(this).transition().duration(150).attr("r", 4);

        // Append a text element near the circle
        svg
          .append("text")
          .attr("id", "hover-text")
          .attr("x", x(d.time) + 10) // Adjust the x position of the text
          .attr("y", y(d.amplitude) - 10) // Adjust the y position of the text
          .attr("text-anchor", "middle")
          .attr("font-size", "12px")
          .attr("fill", "black")
          .text(`Timing: ${getTimeDifference(d, data)}ms`);
      })
      .on("mouseout", function (event, d) {
        // Restore the circle's radius
        d3.select(this)
          .transition()
          .duration(100)
          .attr("r", (d) => (d.position === 0 ? 3 : 1.5));

        // Remove the hover text
        svg.select("#hover-text").remove();
      });

    // Append the SVG element to the container
    const container = document.getElementById("container");
    container.append(svg.node());
  } catch (error) {
    console.error("Error loading data:", error);
  }
};

getData();
