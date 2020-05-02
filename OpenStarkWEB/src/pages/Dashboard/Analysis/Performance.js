import React, { Component } from 'react';
import { connect } from 'dva';
import { Card, Tabs, DatePicker, Input, Table, Divider, Popconfirm, message } from 'antd';
import { TimelineChart } from '@/components/Charts';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import { getTimeDistance } from '@/utils/utils';
import styles from './analysis.less';
import { AsyncLoadBizCharts } from '@/components/Charts/AsyncLoadBizCharts';

const { TabPane } = Tabs;
const { RangePicker } = DatePicker;
const { TextArea, Search } = Input;

@connect(({ chart, loading }) => ({
  chart,
  loading: loading.effects['chart/fetchLoad'],
  apiLoading: loading.effects['chart/fetchLoadAPI'],
  apiEditLoading: loading.effects['chart/editLoadAPI'],
}))
class PerformanceAnalysis extends Component {
  index = 0;

  cacheOriginData = {};

  state = {
    rangePickerValue: getTimeDistance('year'),
    currentTabKey: '',
    data: [],
    page: 1,
    size: 10,
    total: 0,
  };

  componentDidMount() {
    const { dispatch } = this.props;
    const { rangePickerValue } = this.state;
    this.reqRef = requestAnimationFrame(() => {
      dispatch({
        type: 'chart/fetchLoad',
        payload: {
          type: 'load',
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        },
      });
      dispatch({
        type: 'chart/fetchLoadAPI',
        payload: {
          type: 'load',
          startTime: rangePickerValue[0].format('YYYY-MM-DD'),
          endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        },
        op: 'api',
      });
    });
  }

  componentWillReceiveProps(nextProps) {
    if ('chart' in nextProps && nextProps.chart.apiList) {
      this.setState({
        data: nextProps.chart.apiList.data,
        total: nextProps.chart.apiList.total,
        page: nextProps.chart.apiList.page,
        size: nextProps.chart.apiList.size,
      });
    }
  }

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'chart/clear',
    });
    cancelAnimationFrame(this.reqRef);
  }

  onSearchChange = string => {
    const { dispatch } = this.props;
    const { rangePickerValue } = this.state;
    dispatch({
      type: 'chart/fetchLoadAPI',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        kw: string,
      },
      op: 'api',
    });
  };

  getRowByKey(key, newData) {
    const { data } = this.state;
    return (newData || data).filter(item => item.key === key)[0];
  }

  toggleEditable = (e, key) => {
    e.preventDefault();
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      // 进入编辑状态时保存原始数据
      if (!target.editable) {
        this.cacheOriginData[key] = { ...target };
      }
      target.editable = !target.editable;
      this.setState({ data: newData });
    }
  };

  handleRangePickerChange = rangePickerValue => {
    const { dispatch, chart } = this.props;
    const { loadEvn } = chart;
    const { currentTabKey, page, size } = this.state;
    this.setState({
      rangePickerValue,
    });
    dispatch({
      type: 'chart/fetchLoad',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        env: currentTabKey || (loadEvn[0] && loadEvn[0].id),
      },
    });
    dispatch({
      type: 'chart/fetchLoadAPI',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        env: currentTabKey || (loadEvn[0] && loadEvn[0].id),
        page,
        size,
      },
      op: 'api',
    });
  };

  handleTabChange = key => {
    const { dispatch } = this.props;
    const { rangePickerValue, page, size } = this.state;
    this.setState({
      currentTabKey: key,
    });
    dispatch({
      type: 'chart/fetchLoad',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        env: key,
      },
    });
    dispatch({
      type: 'chart/fetchLoadAPI',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        env: key,
        page,
        size,
      },
      op: 'api',
    });
  };

  selectDate = type => {
    const { dispatch, chart } = this.props;
    const { loadEvn } = chart;
    const { currentTabKey, page, size } = this.state;
    this.setState({
      rangePickerValue: getTimeDistance(type),
    });
    dispatch({
      type: 'chart/fetchLoad',
      payload: {
        type: 'load',
        startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
        endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
        env: currentTabKey || (loadEvn[0] && loadEvn[0].id),
      },
    });
    dispatch({
      type: 'chart/fetchLoadAPI',
      payload: {
        type: 'load',
        startTime: getTimeDistance(type)[0].format('YYYY-MM-DD'),
        endTime: getTimeDistance(type)[1].format('YYYY-MM-DD'),
        env: currentTabKey || (loadEvn[0] && loadEvn[0].id),
        page,
        size,
      },
      op: 'api',
    });
  };

  handleTableChange = pagination => {
    const {
      chart: { loadEvn },
      dispatch,
    } = this.props;
    const { currentTabKey, rangePickerValue } = this.state;
    this.setState({
      page: pagination.current,
      size: pagination.pageSize,
    });
    dispatch({
      type: 'chart/fetchLoadAPI',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        env: currentTabKey || (loadEvn[0] && loadEvn[0].id),
        page: pagination.current,
        size: pagination.pageSize,
      },
      op: 'api',
    });
  };

  handleFieldChange(e, fieldName, key) {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      const value = e.target ? e.target.value : e;
      target[fieldName] = value;
      this.setState({ data: newData });
    }
  }

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  cancel(e, key) {
    this.clickedCancel = true;
    e.preventDefault();
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (this.cacheOriginData[key]) {
      Object.assign(target, this.cacheOriginData[key]);
      target.editable = false;
      delete this.cacheOriginData[key];
    }
    this.setState({ data: newData });
    this.clickedCancel = false;
  }

  saveRow(e, key) {
    e.persist();
    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const { rangePickerValue, currentTabKey, page, size } = this.state;
    const target = this.getRowByKey(key) || {};
    if (!target.id || !target.name || !target.showName || !target.api) {
      message.error('请填写完整的接口信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const {
      dispatch,
      chart: { loadEvn },
    } = this.props;
    dispatch({
      type: 'chart/editLoadAPI',
      payload: {
        type: 'sLoad',
        ...target,
      },
      op: 'edit',
    });
    dispatch({
      type: 'chart/fetchLoadAPI',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        env: currentTabKey || (loadEvn[0] && loadEvn[0].id),
        page,
        size,
      },
      op: 'api',
    });
    target.editable = false;
  }

  remove(record) {
    const { data, rangePickerValue, currentTabKey, page, size } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    const {
      dispatch,
      chart: { loadEvn },
    } = this.props;
    this.setState({ data: newData });
    dispatch({
      type: 'chart/editLoadAPI',
      payload: {
        type: 'sLoad',
        ...record,
      },
      op: 'delete',
    });
    dispatch({
      type: 'chart/fetchLoadAPI',
      payload: {
        type: 'load',
        startTime: rangePickerValue[0].format('YYYY-MM-DD'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD'),
        env: currentTabKey || (loadEvn[0] && loadEvn[0].id),
        page,
        size,
      },
      op: 'api',
    });
  }

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
    const { rangePickerValue, currentTabKey, total, page, data } = this.state;
    const { chart, loading, apiLoading, apiEditLoading } = this.props;
    const { loadNames, loadData, loadEvn } = chart;
    const salesExtra = (
      <div className={styles.salesExtraWrap}>
        <div className={styles.salesExtra}>
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

    const activeKey = currentTabKey || (loadEvn[0] && loadEvn[0].id);
    const lastLoadData = loadData && loadData[loadData.length - 1];
    const columns = [
      {
        title: '#',
        dataIndex: 'key',
        key: 'key',
        width: '4%',
        render: text => text,
      },
      {
        title: '测试环境',
        dataIndex: 'env',
        key: 'env',
        width: '10%',
        render: text => text,
      },
      {
        title: '接口标识',
        dataIndex: 'name',
        key: 'id',
        width: '10%',
        render: text => text,
      },
      {
        title: '接口名称',
        dataIndex: 'showName',
        key: 'showName',
        width: '12%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                autoFocus
                value={text}
                onChange={e => this.handleFieldChange(e, 'showName', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="接口名称"
              />
            );
          }
          return text;
        },
      },
      {
        title: '接口地址',
        dataIndex: 'api',
        key: 'api',
        width: '25%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'api', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="接口地址"
              />
            );
          }
          return text;
        },
      },
      {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        width: '20%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <TextArea
                value={text}
                onChange={e => this.handleFieldChange(e, 'description', record.key)}
                placeholder="接口描述"
              />
            );
          }
          let desc = '';
          if (record.env === activeKey) {
            const key = Object.keys(loadNames).filter(
              item => loadNames[item] === record.name || loadNames[item] === record.showName
            );
            let tps = 0;
            if (key.length > 0) {
              tps = lastLoadData[key[0]];
            }
            desc = desc
              .concat('最近版本在')
              .concat(record.userNum)
              .concat('个并发下的平均事务响应时间为')
              .concat(tps)
              .concat('ms')
              .concat(text && '\n'.concat(text));
          } else {
            desc = text;
          }
          return (
            <TextArea
              value={desc}
              style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
              placeholder="接口描述"
              disabled
            />
          );
        },
      },
      {
        title: '并发数',
        dataIndex: 'userNum',
        key: 'userNum',
        width: '6%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'userNum', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="并发数"
              />
            );
          }
          return text;
        },
      },
      {
        title: '达标阈值',
        dataIndex: 'threshold',
        key: 'threshold',
        width: '6%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'threshold', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="达标阈值"
              />
            );
          }
          return text;
        },
      },
      {
        title: '操作',
        key: 'action',
        render: (text, record) => {
          if (!!record.editable && apiEditLoading) {
            return null;
          }
          if (record.editable) {
            return (
              <span>
                <a onClick={e => this.saveRow(e, record.key)}>保存</a>
                <Divider type="vertical" />
                <a onClick={e => this.cancel(e, record.key)}>取消</a>
              </span>
            );
          }
          return (
            <span>
              <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
              <Divider type="vertical" />
              <Popconfirm
                title="统计数据将被清空, 是否要删除此行？"
                onConfirm={() => this.remove(record)}
              >
                <a>删除</a>
              </Popconfirm>
            </span>
          );
        },
      },
    ];

    return (
      <PageHeaderWrapper>
        <Card
          title="性能测试结果汇总统计"
          loading={loading}
          bordered={false}
          bodyStyle={{ padding: 0 }}
          extra={salesExtra}
        >
          <div className={styles.salesCard}>
            <Tabs
              activeKey={activeKey}
              onChange={this.handleTabChange}
              size="large"
              tabBarStyle={{ marginBottom: 24 }}
            >
              {loadEvn.map(item => (
                <TabPane tab={item.name} key={item.id}>
                  <div style={{ padding: '0 24px' }}>
                    <TimelineChart
                      title="响应时间(ms)"
                      height={600}
                      data={loadData}
                      titleMap={loadNames}
                    />
                  </div>
                </TabPane>
              ))}
            </Tabs>
          </div>
        </Card>
        <Card
          title="性能测试接口汇总"
          style={{ marginTop: 32 }}
          extra={
            <Search placeholder="按名称/接口/描述搜索" onSearch={this.onSearchChange} enterButton />
          }
        >
          <Table
            loading={apiLoading || apiEditLoading}
            columns={columns}
            dataSource={data}
            pagination={{
              showSizeChanger: true,
              showQuickJumper: true,
              hideOnSinglePage: true,
              current: page,
              total,
              showTotal: () => '共 '.concat(total).concat(' 条'),
            }}
            onChange={this.handleTableChange}
            rowClassName={record => (record.editable ? styles.editable : '')}
          />
        </Card>
      </PageHeaderWrapper>
    );
  }
}

export default props => (
  <AsyncLoadBizCharts>
    <PerformanceAnalysis {...props} />
  </AsyncLoadBizCharts>
);
