import React from 'react';
import { Chart, Tooltip, Geom, Legend, Axis } from 'bizcharts';
import DataSet from '@antv/data-set';
import Slider from 'bizcharts-plugin-slider';
import autoHeight from '../autoHeight';
import styles from './index.less';

@autoHeight()
class TimelineChart extends React.Component {
  render() {
    const {
      title,
      height = 400,
      padding = [60, 20, 40, 60],
      titleMap = {
        y1: 'y1',
        y2: 'y2',
      },
      borderWidth = 2,
      data: sourceData,
    } = this.props;

    const data = Array.isArray(sourceData) ? sourceData : [{ x: 0, y1: 0, y2: 0 }];

    data.sort((a, b) => a.x - b.x);

    let yCount = 0;

    function getMax(colData) {
      let max;
      if (colData[0] && colData[0].y1 && colData[0].y2) {
        colData.forEach(ele => {
          const num = [];
          const d = ele;
          let tmpMax = 0;
          Object.keys(d).forEach(key => {
            if (key !== 'x') {
              num.push(ele[key]);
            }
          });
          [tmpMax] = num.sort((a, b) => b - a);
          yCount = num.length;
          max = Math.max(max || 0, tmpMax || 0);
        });
      }
      return max;
    }

    let max = getMax(data);

    const ds = new DataSet({
      state: {
        start: data[0].x,
        end: data[data.length - 1].x,
        max,
      },
    });

    let fields = [];
    Object.keys(titleMap).forEach(key => {
      fields.push(titleMap[key]);
    });
    if (fields.length === 0) {
      fields = [titleMap.y1, titleMap.y2];
    }

    const dv = ds.createView();
    dv.source(data)
      .transform({
        type: 'filter',
        callback: obj => {
          const date = obj.x;
          return date <= ds.state.end && date >= ds.state.start;
        },
      })
      .transform({
        type: 'map',
        callback(row) {
          const newRow = { ...row };
          Object.keys(titleMap).forEach(key => {
            newRow[titleMap[key]] = row[key];
          });
          return newRow;
        },
      })
      .transform({
        type: 'fold',
        fields, // 展开字段集
        key: 'key', // key字段
        value: 'value', // value字段
      });

    const timeScale = {
      type: 'time',
      tickInterval: 60 * 60 * 1000 * 24,
      mask: 'YYYY-MM-DD',
      range: [0, 1],
    };

    const cols = {
      x: timeScale,
      value: {
        max,
        min: 0,
      },
    };

    function changeMax(items) {
      const num = [];
      let tmpMax = max;
      items.forEach(item => {
        num.push(parseFloat(item.value));
      });
      [tmpMax] = num.sort((a, b) => b - a);
      max = Math.max(max, tmpMax);
      if (yCount !== num.length) {
        yCount = num.length;
        max = tmpMax;
      }
      if (ds.state.max && ds.state.max !== max) {
        cols.value.max = max;
        ds.setState('max', max);
      }
    }

    const SliderGen = () => (
      <Slider
        padding={[0, padding[1] + 20, 0, padding[3]]}
        width="auto"
        height={26}
        xAxis="x"
        yAxis="y1"
        scales={{ x: timeScale }}
        data={data}
        start={ds.state.start}
        end={ds.state.end}
        backgroundChart={{ type: 'line' }}
        onChange={({ startValue, endValue }) => {
          ds.setState('start', startValue);
          ds.setState('end', endValue);
        }}
      />
    );

    return (
      <div className={styles.timelineChart} style={{ height: height + 60 }}>
        <div>
          {title && <h4>{title}</h4>}
          <Chart
            height={height}
            padding={padding}
            data={dv}
            scale={cols}
            forceFit
            onTooltipChange={e => {
              changeMax(e.items);
            }}
          >
            <Axis name="x" />
            <Tooltip />
            <Legend name="key" position="top" />
            <Geom type="line" position="x*value" size={borderWidth} color="key" />
          </Chart>
          <div style={{ marginRight: -20 }}>
            <SliderGen />
          </div>
        </div>
      </div>
    );
  }
}

export default TimelineChart;
