import React, { PureComponent } from 'react';
import { Select, Spin } from 'antd';
import { connect } from 'dva';
import styles from '../style.less';

const { Option } = Select;

@connect(({ environment, tools, loading }) => ({
  server: environment.envList.data || [],
  detail: environment.detailList.data || [],
  config: tools.configList,
  loading: loading.effects['environment/fetchEnv'],
}))
class EnvView extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      server: undefined,
      detail: [],
      config: undefined,
      lastType: [],
    };
  }

  componentDidMount = () => {
    const { dispatch } = this.props;
    dispatch({
      type: 'environment/fetchEnv',
      op: 'server',
      action: 'all',
    });
  };

  componentWillReceiveProps(nextProps) {
    const { lastType } = this.state;
    if ('type' in nextProps && nextProps.type !== lastType) {
      this.setState({ detail: [], config: undefined, lastType: nextProps.type });
    }
  }

  componentDidUpdate(props) {
    const { dispatch, value, id } = this.props;
    if (!props.value && !!value && !!value.server) {
      dispatch({
        type: 'environment/fetchEnvDetail',
        op: 'detail',
        action: 'all',
        payload: {
          eid: value.server.key,
          type: id === 'envSQL' ? 'APPLICATION' : 'OS',
        },
      });
    }
  }

  getServerOption() {
    const { server, id } = this.props;
    if (id === 'source') {
      return this.getOption(server.filter(item => item.title.search('准生产') !== -1));
    }
    if (id === 'target' || id === 'reTarget') {
      return this.getOption(server.filter(item => item.title.search('准生产') === -1));
    }
    return this.getOption(server);
  }

  getDetailOption = () => {
    const { detail, type, id } = this.props;
    if (id === 'source') {
      return this.getOption(detail.filter(item => item.id && item.id.slice(-2) === '17'));
    }
    if (id === 'target' || id === 'reTarget') {
      return this.getOption(detail.filter(item => item.id && item.id.slice(-1) === '4'));
    }
    if (type && type.length) {
      return this.getOption(detail.filter(item => item.id && type.includes(item.id.slice(-1))));
    }
    return this.getOption(detail);
  };

  getConfigOption = () => {
    const { config } = this.props;
    if (!config || config.length < 1) {
      return (
        <Option key={0} value={0}>
          没有找到选项
        </Option>
      );
    }
    return config.map(item => (
      <Option key={item} value={item} title={item}>
        {item}
      </Option>
    ));
  };

  getOption = list => {
    if (!list || list.length < 1) {
      return (
        <Option key={0} value={0}>
          没有找到选项
        </Option>
      );
    }
    return list.map(item => (
      <Option key={item.key} value={item.id} title={item.description}>
        {item.title}
      </Option>
    ));
  };

  selectServerItem = item => {
    const { dispatch, onChange, id } = this.props;
    dispatch({
      type: 'environment/fetchEnvDetail',
      op: 'detail',
      action: 'all',
      payload: {
        eid: item.key,
        type: id === 'envSQL' ? 'APPLICATION' : 'OS',
      },
    });
    this.setState({ server: item, detail: [], config: undefined });
    onChange({
      server: item,
      detail: [],
      config: undefined,
    });
  };

  selectDetailItem = item => {
    if (item.key !== 0) {
      const { value, onChange, id, dispatch, type } = this.props;
      const { detail } = this.state;
      if (id === 'reTarget') {
        dispatch({
          type: 'tools/fetchConfig',
          payload: {
            queryIp: item.key,
          },
        });
      }
      detail.push(item);
      this.setState({ detail: type && type.length > 1 ? detail : [item], config: undefined });
      onChange({
        server: value && value.server,
        detail: type && type.length > 1 ? detail : [item],
        config: undefined,
      });
    }
  };

  onDeselectDetailItem = item => {
    if (item.key !== 0) {
      const { value, onChange, id, dispatch } = this.props;
      const { detail } = this.state;
      if (id === 'reTarget') {
        dispatch({
          type: 'tools/fetchConfig',
          payload: {
            queryIp: item.key,
          },
        });
      }
      this.setState({ detail: detail.filter(ele => ele.key !== item.key), config: undefined });
      onChange({
        server: value && value.server,
        detail: detail.filter(ele => ele.key !== item.key),
        config: undefined,
      });
    }
  };

  selectConfigItem = item => {
    const { value, onChange } = this.props;
    this.setState({ config: item });
    onChange({
      server: value && value.server,
      detail: value && value.detail,
      config: item,
    });
  };

  render() {
    const { server, detail, config } = this.state;
    const { loading, id, type } = this.props;
    const ReSelect = (
      <Select
        className={styles.item}
        value={config}
        labelInValue
        showSearch
        onSelect={this.selectConfigItem}
        placeholder="请选择要还原的配置文件"
        style={{ width: '100%' }}
      >
        {this.getConfigOption()}
      </Select>
    );
    return (
      <Spin spinning={loading} wrapperClassName={styles.row}>
        <Select
          className={styles.item}
          value={server}
          labelInValue
          showSearch
          onSelect={this.selectServerItem}
          placeholder="请选择测试环境"
          style={{ width: '100%' }}
        >
          {this.getServerOption()}
        </Select>
        <Select
          className={styles.item}
          value={detail}
          labelInValue
          showSearch
          mode={type && type.length > 1 ? 'multiple' : '-'}
          onSelect={this.selectDetailItem}
          onDeselect={this.onDeselectDetailItem}
          placeholder="请选择具体服务器"
          style={{ width: '100%' }}
        >
          {this.getDetailOption()}
        </Select>
        {id === 'reTarget' ? ReSelect : ''}
      </Spin>
    );
  }
}

export default EnvView;
