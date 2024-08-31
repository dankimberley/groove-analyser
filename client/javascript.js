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
  const simultaneousTransients = findSimlutaneousTransients(data)
  const timingDifferences = getTimingDifferences(simultaneousTransients)
  const averageTimingDifference = timingDifferences.reduce((a, b) => a + b) / timingDifferences.length
  text.textContent = `${Math.round(averageTimingDifference)}ms average`
}

const findSimlutaneousTransients = (data) => {
  const primaryTransients = data.grid.map((point) => point.time)
  const secondaryTransients = data.points
  const simultaneous = []

  secondaryTransients.forEach((secondaryTransient) => {
    primaryTransients.forEach((primaryTransient) => {
      if (Math.abs(primaryTransient - secondaryTransient.time) < 50) {
        simultaneous.push({'primary':primaryTransient, 'secondary':secondaryTransient.time})
      }
    })
  })
  console.log(simultaneous)
  return simultaneous
}

const getTimingDifferences = (simultaneousTransients) => {
  const differences = []
  simultaneousTransients.forEach((transient) => {
    differences.push(transient.secondary - transient.primary)
  })
  return differences
}



getData();
