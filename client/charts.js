let svg;
let x;
let y;
let height;
let width;
let marginTop;
let marginBottom;
let marginRight;
let marginLeft;
let localDomainUpper
let localDomainLower

const getTimeDifference = (point, grid) => {
  let inputOnset = point.time;
  let gridOnset = grid.grid.find(
    (item) => item.bar === point.bar && item.position === point.position
  ).time;
  return inputOnset - gridOnset;
};

const colourScale = d3.scaleLinear().domain([localDomainLower, localDomainUpper]).range(["blue", "red"]);
const getColour = (value) => colourScale(value);

const createChart = (domainLower, domainUpper, length) => {
  width = 1000;
  height = 400;
  marginTop = 20;
  marginRight = 20;
  marginBottom = 30;
  marginLeft = 40;

  localDomainLower = domainLower
  localDomainUpper = domainUpper

  x = d3
    .scaleLinear()
    .domain([0, length]) // Set the x-axis domain from 0 to 12000
    .range([marginLeft, width - marginRight]);

  y = d3
    .scaleLinear()
    .domain([domainLower > -120 ? domainLower : -120, domainUpper])
    .range([height - marginBottom, marginTop]);

  svg = d3.create("svg").attr("width", width).attr("height", height);

  document.getElementById("container").appendChild(svg.node());

  svg
    .append("g")
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(x));

  // Add the y-axis.
  svg
    .append("g")
    .attr("transform", `translate(${marginLeft},0)`)
    .call(d3.axisLeft(y));
};

export const createGrid = (data) => {
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
};

const createWaveform = (data) => {
  svg
    .append("path")
    .datum(data.waveform)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 0.4)
    .attr(
      "d",
      d3
        .line()
        .curve(d3.curveBasis)
        .x(function (d) {
          return x(d.time);
        })
        .y(function (d) {
          return y(d.amplitude);
        })
    );
};

export const createPoints = (data) => {
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
      svg
        .append("text")
        .attr("id", "hover-text")
        .attr("x", x(d.time) + 10) // Adjust the x position of the text
        .attr("y", y(d.amplitude) - 10) // Adjust the y position of the text
        .attr("text-anchor", "middle")
        .attr("font-size", "12px")
        .attr("fill", "black")
        .text(
          `Time: ${d.time}ms Amplitude: ${
            d.amplitude
          } Timing: ${getTimeDifference(d, data)}ms`
        );
    })
    .on("mouseout", function (event, d) {
      // Remove the hover text
      svg.select("#hover-text").remove();
    });
};

export { createChart, createWaveform };
