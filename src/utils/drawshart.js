import { Chart, registerables } from "chart.js"
import moment from "moment"
import 'chartjs-adapter-moment'

Chart.register(...registerables)

export default function initChart(element, datas) {
    if (!datas) return

    const prevInst = Object.values(Chart.instances).filter(c => c.canvas.id == element).pop()

    if (prevInst) prevInst.destroy()
  
    if (moment(datas.end_date).diff(datas.start_date, 'day') <= 365) {
        new Chart(element, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: "Current period",
                        data: datas.chart_datas.map(x => { return { x: x.date.slice(5), y: x.count } }),
                        fill: true
                    },
                    {
                        label: 'Previous period',
                        data: datas.prev_period.prev_chart.map(x => { return { x: x.date.slice(5), y: x.count } }),
                        fill: true
                    }
                ],
            },
            options: {
                scales: {
                    xAxis: {
                        type: 'time',
                        time: {
                            parser: 'MM-DD',
                            tooltipFormat: 'MMM DD',
                            unit: 'day',
                          }
                    }
                }
            }
        })    
  
        return
    }
    else {
        new Chart('stats-chart', {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: "Current period",
                        data: datas.chart_datas.map(x => { return { x: x.date, y: x.count } }),
                        fill: true
                    },
                    {
                        label: 'Previous period',
                        data: datas.prev_period.prev_chart.map(x => { return { x: x.date, y: x.count } }),
                        fill: true
                    }
                ]
            },
            options: {
                scales: {
                    xAxis: {
                        type: 'time',
                        time: {
                            parser: 'YYYY-MM-DD',
                            tooltipFormat: 'YYYY MMM DD',
                            unit: 'month',
                          }
                    }
                },
                responsive: true,
            }
        })
    }

}