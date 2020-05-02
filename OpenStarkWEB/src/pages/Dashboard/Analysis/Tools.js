import React, { Component } from 'react';
import { connect } from 'dva';
import { Row, Col, Card, Tabs, DatePicker } from 'antd';
import numeral from 'numeral';
import { Bar, Pie, TimelineChart } from '@/components/Charts';
import NumberInfo from '@/components/NumberInfo';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import { getTimeDistance } from '@/utils/utils';
import styles from './analysis.less';
import { AsyncLoadBizCharts } from '@/components/Charts/AsyncLoadBizCharts';

const { TabPane } = Tabs;
const { RangePicker } = DatePicker;

@connect(({ chart, loading }) => ({
  chart,
  loading: loading.effects['chart/fetch'],
}))
class ToolsAnalysis extends Component {
  state = {
    currentTabKey: '',
    rangePickerValue: getTimeDistance('month'),
  };

  componentDidMount() {
    const { dispatch } = this.props;
    const { rangePickerValue } = this.state;
    this.reqRef = requestAnimationFrame(() => {
      dispatch({
        type: 'chart/fetch',
        payload: [
          {
            type: 'pv',
            startTime: rangePickerValue[0].format('YYYY-MM-DD'),
            endTime: rangePickerValue[1].format('YYYY-MM-DD'),
          },
        ],
      });
      dispatch({
        type: 'chart/fetch',
        payload: [
          {
            type: 'active',
            startTime: rangePickerValue[0].format('YYYY-MM-DD'),
            endTime: rangePickerValue[1].format('YYYY-MM-DD'),
          },
        ],
      });
      dispatch({
        type: 'chart/fetch',
        payload: [
          {
            type: 'data',
            startTime: rangePickerValue[0].format('YYYY-MM-DD'),
            endTime: rangePickerValue[1].format('YYYY-MM-DD'),
          },
        ],
      });
    });
  }

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'chart/clear',
    });
    cancelAnimationFrame(this.reqRef);
  }

  handleTabChange = key => {
    const { dispatch } = this.props;
    const { rangePickerValue } = this.state;
    this.setState({
      currentTabKey: key,
    });
    dispatch({
      type: 'chart/fetch',
      payload: [
        {
          pid: key,
          type: 'data',
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        },
      ],
    });
  };

  handleRangePickerChange = rangePickerValue => {
    const { dispatch } = this.props;
    const { currentTabKey } = this.state;
    this.setState({
      rangePickerValue,
    });
    dispatch({
      type: 'chart/fetch',
      payload: [
        {
          type: 'pv',
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        },
      ],
    });
    dispatch({
      type: 'chart/fetch',
      payload: [
        {
          type: 'active',
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        },
      ],
    });
    dispatch({
      type: 'chart/fetch',
      payload: [
        {
          type: 'data',
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
          pid: currentTabKey,
        },
      ],
    });
  };

  selectDate = type => {
    const { dispatch } = this.props;
    const { currentTabKey } = this.state;
    this.setState({
      rangePickerValue: getTimeDistance(type),
    });
    dispatch({
      type: 'chart/fetch',
      payload: [
        {
          type: 'pv',
          startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
          endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
        },
      ],
    });
    dispatch({
      type: 'chart/fetch',
      payload: [
        {
          type: 'active',
          startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
          endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
        },
      ],
    });
    dispatch({
      type: 'chart/fetch',
      payload: [
        {
          type: 'data',
          startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
          endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
          pid: currentTabKey,
        },
      ],
    });
  };

  isActive(type) {
    const { rangePickerValue } = this.state;
    const value = getTimeDistance(type);
    if (!rangePickerValue[0] || !rangePickerValue[1]) {
      return '';
    }
    if (
      rangePickerValue[0].isSame(value[0], 'day') &&
      rangePickerValue[1].isSame(value[1], 'day')
    ) {
      return styles.currentDate;
    }
    return '';
  }

  render() {
    const { rangePickerValue, currentTabKey } = this.state;
    const { chart, loading } = this.props;
    const {
      toolsPVRange,
      toolsActiveRange,
      toolsPVRanking,
      toolsActiveRanking,
      toolsRangeData,
      toolsList,
    } = chart;

    const salesExtra = (
      <div className={styles.salesExtraWrap}>
        <div className={styles.salesExtra}>
          <a className={this.isActive('today')} onClick={() => this.selectDate('today')}>
            今日
          </a>
          <a className={this.isActive('week')} onClick={() => this.selectDate('week')}>
            本周
          </a>
          <a className={this.isActive('month')} onClick={() => this.selectDate('month')}>
            本月
          </a>
          <a className={this.isActive('year')} onClick={() => this.selectDate('year')}>
            全年
          </a>
        </div>
        <RangePicker
          allowClear={false}
          value={rangePickerValue}
          onChange={this.handleRangePickerChange}
          style={{ width: 256 }}
        />
      </div>
    );

    const activeKey = currentTabKey || (toolsList[0] && toolsList[0].id);
    const CustomTab = ({ data, currentTabKey: currentKey }) => (
      <Row gutter={8} style={{ width: 138, margin: '8px 0' }}>
        <Col span={12}>
          <NumberInfo
            title={data.name}
            subTitle="转化率"
            gap={2}
            total={`${parseFloat(
              (
                ((toolsActiveRanking.filter(item => item.id === data.id).length > 0
                  ? toolsActiveRanking.filter(item => item.id === data.id)[0].total
                  : 0) /
                  (toolsPVRanking.filter(item => item.id === data.id).length > 0
                    ? toolsPVRanking.filter(item => item.id === data.id)[0].total
                    : 1)) *
                100
              ).toFixed(0)
            )}%`}
            theme={currentKey !== data.id && 'light'}
          />
        </Col>
        <Col span={12} style={{ paddingTop: 36 }}>
          <Pie
            animate={false}
            color={currentKey !== data.id && '#BDE4FF'}
            inner={0.55}
            tooltip={false}
            margin={[0, 0, 0, 0]}
            percent={parseFloat(
              (
                ((toolsActiveRanking.filter(item => item.id === data.id).length > 0
                  ? toolsActiveRanking.filter(item => item.id === data.id)[0].total
                  : 0) /
                  (toolsPVRanking.filter(item => item.id === data.id).length > 0
                    ? toolsPVRanking.filter(item => item.id === data.id)[0].total
                    : 1)) *
                100
              ).toFixed(0)
            )}
            height={64}
          />
        </Col>
      </Row>
    );

    return (
      <PageHeaderWrapper>
        <Card loading={loading} bordered={false} bodyStyle={{ padding: 0 }}>
          <div className={styles.salesCard}>
            <Tabs tabBarExtraContent={salesExtra} size="large" tabBarStyle={{ marginBottom: 24 }}>
              <TabPane tab="工具浏览量" key="pv">
                <Row>
                  <Col xl={16} lg={12} md={12} sm={24} xs={24}>
                    <div className={styles.salesBar}>
                      <Bar height={295} title="浏览量(PV)" data={toolsPVRange} />
                    </div>
                  </Col>
                  <Col xl={8} lg={12} md={12} sm={24} xs={24}>
                    <div className={styles.salesRank}>
                      <h4 className={styles.rankingTitle}>浏览量排名</h4>
                      <ul className={styles.rankingList}>
                        {toolsPVRanking.slice(0, 7).map((item, i) => (
                          <li key={item.title}>
                            <span
                              className={`${styles.rankingItemNumber} ${
                                i < 3 ? styles.active : ''
                              }`}
                            >
                              {i + 1}
                            </span>
                            <span className={styles.rankingItemTitle} title={item.title}>
                              {item.title}
                            </span>
                            <span className={styles.rankingItemValue}>
                              {numeral(item.total).format('0,0')}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </Col>
                </Row>
              </TabPane>
              <TabPane tab="工具使用量" key="active">
                <Row>
                  <Col xl={16} lg={12} md={12} sm={24} xs={24}>
                    <div className={styles.salesBar}>
                      <Bar height={292} title="使用量" data={toolsActiveRange} />
                    </div>
                  </Col>
                  <Col xl={8} lg={12} md={12} sm={24} xs={24}>
                    <div className={styles.salesRank}>
                      <h4 className={styles.rankingTitle}>使用量排名</h4>
                      <ul className={styles.rankingList}>
                        {toolsActiveRanking.slice(0, 7).map((item, i) => (
                          <li key={item.title}>
                            <span
                              className={`${styles.rankingItemNumber} ${
                                i < 3 ? styles.active : ''
                              }`}
                            >
                              {i + 1}
                            </span>
                            <span className={styles.rankingItemTitle} title={item.title}>
                              {item.title}
                            </span>
                            <span className={styles.rankingItemValue}>
                              {numeral(item.total).format('0,0')}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </Col>
                </Row>
              </TabPane>
            </Tabs>
          </div>
        </Card>
        <Card
          loading={loading}
          className={styles.offlineCard}
          bordered={false}
          bodyStyle={{ padding: '0 0 32px 0' }}
          style={{ marginTop: 32 }}
        >
          <Tabs activeKey={activeKey} onChange={this.handleTabChange}>
            {toolsList.map(shop => (
              <TabPane tab={<CustomTab data={shop} currentTabKey={activeKey} />} key={shop.id}>
                <div style={{ padding: '0 24px' }}>
                  <TimelineChart
                    height={500}
                    data={toolsRangeData}
                    titleMap={{ y1: '浏览量', y2: '使用量' }}
                  />
                </div>
              </TabPane>
            ))}
          </Tabs>
        </Card>
      </PageHeaderWrapper>
    );
  }
}

export default props => (
  <AsyncLoadBizCharts>
    <ToolsAnalysis {...props} />
  </AsyncLoadBizCharts>
);
