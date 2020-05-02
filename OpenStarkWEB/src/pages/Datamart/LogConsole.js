import React from 'react';
import { Divider, Input, Button, Row, Col } from 'antd';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';

const { TextArea } = Input;

export default class LogConsolePage extends React.Component {
  constructor(props) {
    super(props);

    this.sendOnClick = this.sendOnClick.bind(this);
    this.handelChange = this.handelChange.bind(this);

    this.state = {
      sendMsg: '',
      result: '',
      ws: null,
      client_id: 0,
    };
  }

  componentDidMount() {
    this.connect();
  }

  onclose = () => {
    this.setState({
      ws: null,
    });
  };

  onopen = () => {
    // const { ws } = this.state;
    // ws.send(JSON.stringify({ "op":"echo", "message":"你好，我是AceDou!" }));
  };

  onmessage = ({ data }) => {
    this.setState({ result: data });
    try {
      this.doMessage(data);
    } catch (e) {
      console.log(e);
    }
  };

  clearOnClick = () => {
    this.setState({
      sendMsg: '',
    });
  };

  sendOnClick = type => () => {
    const { ws, sendMsg } = this.state;
    console.log(type, ws);
    if (ws === null) {
      if (type === 100) {
        this.connect();
        return;
      }

      this.setState({
        result: '连接已经断开',
      });
      return;
    }

    if (type === 0) {
      ws.send(JSON.stringify(sendMsg));
    } else if (type === 1) {
      ws.send(
        JSON.stringify({
          op: 'tasks',
        })
      );
    } else if (type === 2) {
      ws.send(
        JSON.stringify({
          op: 'client_id',
        })
      );
    } else if (type === 3) {
      ws.send(
        JSON.stringify({
          op: 'jobs',
        })
      );
    } else if (type === 100) {
      if (ws != null) {
        ws.close();
      }
      this.connect();
    } else if (type === 101) {
      if (ws != null) {
        ws.close();
        this.setState({
          ws: null,
        });
      }
    } else if (type === 999) {
      ws.send(
        JSON.stringify({
          op: 'heart_beat',
          value: new Date().getTime(),
        })
      );
    }
  };

  doMessage(data) {
    const cmd = JSON.parse(data);
    switch (cmd.op) {
      case 'client_id': {
        this.setState({
          client_id: parseInt(cmd.response.client_id),
          result: cmd.response.client_id,
        });
      }
      default: {
      }
    }
  }

  connect() {
    const ws = new WebSocket('ws://172.20.17.136:12345/api/pydata/weblogs');

    ws.onmessage = this.onmessage;
    ws.onclose = this.onclose;
    ws.onopen = this.onopen;
    this.setState({
      ws,
    });
  }

  handelChange(e) {
    this.setState({
      sendMsg: e.target.value,
    });
  }

  render() {
    const { result, sendMsg } = this.state;
    return (
      <PageHeaderWrapper>
        <Divider>消息窗口</Divider>
        <Row gutter={16} type="flex" justify="center">
          <Col span={24}>
            <TextArea
              placeholder=""
              autosize={{ minRows: 5, maxRows: 1024 }}
              value={JSON.stringify(result)}
            />
          </Col>
        </Row>
        <Divider>发送窗口</Divider>
        <Row gutter={16} type="flex" justify="center">
          <Col span={24}>
            <TextArea
              placeholder="发送消息输入窗口，请输入准备发送的消息"
              autosize={{ minRows: 5, maxRows: 1024 }}
              onChange={this.handelChange}
              value={sendMsg}
            />
          </Col>
        </Row>
        <Row gutter={16} type="flex" justify="center">
          <Col span={12}>
            <Button type="primary" onClick={this.sendOnClick(0)} htmlType="button">
              发送
            </Button>
            <Button type="dashed" onClick={this.sendOnClick(1)} htmlType="button">
              tasks
            </Button>
            <Button type="dashed" onClick={this.sendOnClick(2)} htmlType="button">
              client_id
            </Button>
            <Button type="dashed" onClick={this.sendOnClick(3)} htmlType="button">
              jobs
            </Button>
          </Col>
          <Col span={12}>
            <Button type="dashed" onClick={this.sendOnClick(100)} htmlType="button">
              重新连接
            </Button>
            <Button type="dashed" onClick={this.sendOnClick(101)} htmlType="button">
              关闭连接
            </Button>
            <Button type="dashed" onClick={this.sendOnClick(999)} htmlType="button">
              心跳
            </Button>
            <Button type="dashed" onClick={this.clearOnClick} htmlType="button">
              清空
            </Button>
          </Col>
        </Row>
      </PageHeaderWrapper>
    );
  }
}
