import { createGrid } from "./charts.js";
import { createChart, createWaveform, createPoints } from "./charts.js";

const getMinAmplitude = (data) => {
    return data.reduce((prev, curr) =>
      prev.amplitude < curr.amplitude ? prev : curr
    );
  };
  
  const getMaxAmplitude = (data) => {
    return data.reduce((prev, curr) =>
      prev.amplitude > curr.amplitude ? prev : curr
    );
  };
  

const getData = async () => {
  try {
    const response = await fetch("../api/outputs/output.json");
    const data = await response.json()

    console.log(getMaxAmplitude(data.points));

    createChart(getMinAmplitude(data.points).amplitude, getMaxAmplitude(data.points).amplitude, data.points.pop().time);
    createPoints(data)
    createGrid(data)
    writeAnalysis(data)

  } catch (error) {
    console.log("Error loading data :(", error);
  }
};

const writeAnalysis = (data) => {
  const text = document.getElementById('text')
  text.textContent = data.grid[0]['amplitude']
}

getData();
