import { Chart, registerables } from "chart.js"
import moment from "moment"
import 'chartjs-adapter-moment'

Chart.register(...registerables)

export default function initChart(datas, dates) {
    if (!datas) return

    const prevInst = Object.values(Chart.instances).filter(c => c.canvas.id == 'stats-chart').pop()

    if (prevInst) prevInst.destroy()
  
    if (dates.value && moment(dates.value.end_date).diff(dates.value.start_date, 'month') <= 12) {

        let combinedDates = [...new Set(datas.chart_datas.map(x => x.date.slice(5)).concat(datas.prev_period.prev_chart.map(x => x.date.slice(5)).sort()).sort())]
        new Chart('stats-chart', {
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
                // scales: {
                //     xAxis: {
                //         type: 'time'
                //     }
                // },
                responsive: true,
            }
        })
    }

}