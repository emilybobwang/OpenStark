import React, { PureComponent } from 'react';
import { Select, Spin } from 'antd';
import { connect } from 'dva';
import styles from '../style.less';

const { Option } = Select;

@connect(({ environment, jobs, tools, loading }) => ({
  server: environment.envList.data || [],
  dbs: tools.dbList,
  tables: tools.tableList,
  jenkinsApps: jobs.jenkinsApps,
  loading: loading.effects['environment/fetchEnv'],
  dbLoading: loading.effects['tools/fetchDBs'],
  verLoading: loading.effects['tools/getVers'],
}))
class EnvView extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      server: undefined,
      dbs: [],
      tables: [],
      lastType: '',
      display: true,
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
      this.setState({ dbs: [], tables: [], lastType: nextProps.type });
    }
  }

  componentDidUpdate(props) {
    const { dispatch, value } = this.props;
    if (!props.value && !!value && !!value.server) {
      dispatch({
        type: 'tools/fetchDBs',
        op: 'db',
      });
    }
  }

  getServerOption() {
    const { server, id } = this.props;
    if (id === 'source') {
      return this.getOption(server.filter(item => item.title.search('准生产') !== -1));
    }
    if (id === 'target' || id === 'reTarget' || id === 'left' || id === 'appLeft' || id === 'appRight') {
      return this.getOption(server.filter(item => item.title.search('准生产') === -1));
    }
    return this.getOption(server);
  }

  getDBsOption = () => {
    const { dbs, jenkinsApps, id } = this.props;
    if (id === 'appLeft'){
      return this.getOption(jenkinsApps);
    }
    return this.getOption(dbs);
  };

  getTablesOption = () => {
    const { tables } = this.props;
    return this.getOption(tables);
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
    const { dispatch, onChange, id, date } = this.props;
    if (id === 'appLeft' || id === 'appRight') {
      dispatch({
        type: 'jobs/getJenkins',
        op: 'apps',
      });
    }else if (id === 'source' || id === 'reTarget' || id === 'left') {
      dispatch({
        type: 'tools/fetchDBs',
        op: 'db',
        payload: {
          key: item.key,
          date,
        },
      });
    }
    this.setState({ server: item, dbs: [], tables: [] });
    onChange({
      server: item,
      dbs: [],
      tables: [],
    });
  };

  selectDBsItem = item => {
    const { value, onChange, dispatch, id, sameValue } = this.props;
    const { dbs } = this.state;
    if (id !== 'appLeft' && id !== 'appRight'){
      if (item.key !== 0) {
        dbs.push(item);
        if (dbs.length < 2) {
          dispatch({
            type: 'tools/fetchDBs',
            op: 'table',
            payload: {
              key: item.key,
            },
          });
        }
      }
      this.setState({ dbs, tables: [], display: dbs.length < 2 });
      onChange({
        server: value && value.server,
        dbs,
        tables: [],
      });
    }else{
      if (item.key !== 0 && sameValue) {
        dispatch({
          type: 'tools/getVers',
          op: 'version',
          payload: {
            app: item.key,
            key: value && value.server && value.server.key,
          },
        });
      }
      this.setState({ dbs: item, tables: undefined});
      onChange({
        server: value && value.server,
        dbs: item,
        tables: undefined,
      });
    }
  };

  onDeselectDBsItem = item => {
    if (item.key !== 0) {
      const { value, onChange, dispatch } = this.props;
      const { dbs } = this.state;
      let newDBs = [];
      newDBs = dbs.filter(ele => ele.key !== item.key);
      if (newDBs.length < 2 && newDBs.length > 0) {
        dispatch({
          type: 'tools/fetchDBs',
          op: 'table',
          payload: {
            key: newDBs[0].key,
          },
        });
      }
      this.setState({ dbs: newDBs, tables: [], display: newDBs.length < 2 });
      onChange({
        server: value && value.server,
        dbs: newDBs,
        tables: [],
      });
    }
  };

  selectTablesItem = item => {
    const { value, onChange, id } = this.props;
    const { tables } = this.state;
    if (id !== 'appLeft' && id !== 'appRight'){
      if (item.key !== 0) {
        tables.push(item);
      }
      this.setState({ tables });
      onChange({
        server: value && value.server,
        dbs: value && value.dbs,
        tables,
      });
    }else{
      this.setState({ tables: item });
      onChange({
        server: value && value.server,
        dbs: value && value.dbs,
        tables: item,
      });
    }
  };

  onDeselectTablesItem = item => {
    if (item.key !== 0) {
      const { value, onChange } = this.props;
      const { tables } = this.state;
      let newTables = [];
      newTables = tables.filter(ele => ele.key !== item.key);
      this.setState({ tables: newTables });
      onChange({
        server: value && value.server,
        dbs: value && value.dbs,
        tables: newTables,
      });
    }
  };

  render() {
    const { server, dbs, tables, display } = this.state;
    const { loading, id, dbLoading, sameValue, verLoading, version } = this.props;
    if (id === 'appLeft' || id === 'appRight'){
      return (
        <Spin spinning={loading || dbLoading || verLoading || false} wrapperClassName={styles.row}>
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
          {id === 'appRight' ? '' : (
            <Select
              className={styles.item}
              value={dbs}
              labelInValue
              showSearch
              onSelect={this.selectDBsItem}
              placeholder="请选择应用包"
              style={{ width: '100%' }}
            >
              {this.getDBsOption()}
            </Select>
          )}
          {!sameValue ? (<span style={{ color: 'red' }}>{version}</span>) : (
            <Select
              className={styles.item}
              value={tables}
              labelInValue
              showSearch
              onSelect={this.selectTablesItem}
              placeholder="请选择应用包版本"
              style={{ width: '100%' }}
            >
              {this.getTablesOption()}
            </Select>
          ) }
        </Spin>
      );
    }
    return (
      <Spin spinning={loading || dbLoading || false} wrapperClassName={styles.row}>
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
        {id === 'source' || id === 'reTarget' || id === 'left' ? (
          <Select
            className={styles.item}
            value={dbs}
            labelInValue
            showSearch
            mode="multiple"
            onSelect={this.selectDBsItem}
            onDeselect={this.onDeselectDBsItem}
            placeholder="请选择数据库"
            style={{ width: '100%' }}
          >
            {this.getDBsOption()}
          </Select>
        ) : (
          ''
        )}
        {(id === 'source' || id === 'left') && display ? (
          <Select
            className={styles.item}
            value={tables}
            labelInValue
            showSearch
            mode="multiple"
            onSelect={this.selectTablesItem}
            onDeselect={this.onDeselectTablesItem}
            placeholder="请选择数据表"
            style={{ width: '100%' }}
          >
            {this.getTablesOption()}
          </Select>
        ) : (
          ''
        )}
      </Spin>
    );
  }
}

export default EnvView;
