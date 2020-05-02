import React, { PureComponent, Fragment } from 'react';
import { Table, Button, Input, message, Popconfirm, Divider } from 'antd';
import styles from '../style.less';

export default class GroupForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('data' in nextProps) {
      this.setState({
        data: nextProps.data,
      });
    }
  }

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

  newMember = () => {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    newData.push({
      key: `NEW_TEMP_ID_${this.index}`,
      company: '',
      cid: '',
      department: '',
      did: '',
      team: '',
      tid: '',
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  remove(record) {
    const { data } = this.state;
    const { removeRow, id } = this.props;
    const newData = data.filter(item => item.key !== record.key);
    this.setState({ data: newData });
    if (typeof record.key === 'number') {
      removeRow({ type: id, data: record });
    }
  }

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  handleFieldChange(e, fieldName, key) {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      target[fieldName] = e.target.value;
      this.setState({ data: newData });
    }
  }

  saveRow(e, key) {
    e.persist();
    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.company || !target.department) {
      message.error('请填写完整的团队信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { saveRow, id } = this.props;
    saveRow({ type: id, data: target });
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

  render() {
    const { loading } = this.props;
    const { data } = this.state;
    const columns = [
      {
        title: '#',
        dataIndex: 'key',
        key: 'key',
        width: '8%',
        render: text => text,
      },
      {
        title: '公司',
        dataIndex: 'company',
        key: 'cid',
        width: '25%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'company', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="公司"
              />
            );
          }
          return text;
        },
      },
      {
        title: '部门',
        dataIndex: 'department',
        key: 'did',
        width: '25%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'department', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="部门"
              />
            );
          }
          return text;
        },
      },
      {
        title: '小组',
        dataIndex: 'team',
        key: 'tid',
        width: '25%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'team', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="小组"
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
          if (!!record.editable && loading) {
            return null;
          }
          if (record.editable) {
            if (record.isNew) {
              return (
                <span>
                  <a onClick={e => this.saveRow(e, record.key)}>添加</a>
                  <Divider type="vertical" />
                  <Popconfirm title="是否要删除此行？" onConfirm={() => this.remove(record)}>
                    <a>删除</a>
                  </Popconfirm>
                </span>
              );
            }
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
              <Popconfirm title="是否要删除此行？" onConfirm={() => this.remove(record)}>
                <a>删除</a>
              </Popconfirm>
            </span>
          );
        },
      },
    ];

    return (
      <Fragment>
        <Table
          loading={loading}
          columns={columns}
          dataSource={data}
          pagination={false}
          rowClassName={record => (record.editable ? styles.editable : '')}
        />
        <Button
          style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
          type="dashed"
          onClick={this.newMember}
          icon="plus"
        >
          新增团队
        </Button>
      </Fragment>
    );
  }
}
