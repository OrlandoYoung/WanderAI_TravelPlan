# 系统架构图

```mermaid
flowchart BT
    %% 定义样式
    classDef layerStyle fill:#f9f,stroke:#333,stroke-width:2px;
    classDef componentStyle fill:#bbf,stroke:#333,stroke-width:1px;
    
    %% 应用展示层 (顶层)
    app[应用展示层]:::layerStyle
    web[Web 告警界面]:::componentStyle
    
    app --> web
    
    %% 检测算法层 (核心层)
    algo[检测算法层]:::layerStyle
    ml[机器学习模型]:::componentStyle
    
    algo --> ml
    
    %% 数据处理层 (中层)
    process[数据处理层]:::layerStyle
    featEng[特征工程 Python 脚本]:::componentStyle
    
    process --> featEng
    
    %% 数据采集层 (底层)
    collect[数据采集层]:::layerStyle
    suricata[Suricata]:::componentStyle
    pcap[PCAP]:::componentStyle
    
    collect --> suricata
    collect --> pcap
    
    %% 层间连接 (数据流向)
    collect --> process
    process --> algo
    algo --> app
    
    %% 标题
    title 入侵检测系统架构图
```

## 架构说明

1. **数据采集层** (底层)
   - 负责从网络中采集原始流量数据
   - 主要组件：
     - Suricata：开源的网络入侵检测系统，实时监控网络流量
     - PCAP：网络数据包捕获文件格式，用于离线分析

2. **数据处理层** (中层)
   - 对采集到的原始数据进行预处理和特征提取
   - 主要组件：
     - 特征工程 Python 脚本：将原始网络数据转换为适合机器学习模型输入的特征向量

3. **检测算法层** (核心层)
   - 利用机器学习模型对处理后的数据进行入侵检测
   - 主要组件：
     - 机器学习模型：基于训练好的模型对网络流量进行分类，识别潜在的入侵行为

4. **应用展示层** (顶层)
   - 将检测结果以直观的方式呈现给用户
   - 主要组件：
     - Web 告警界面：实时展示检测结果，提供告警通知和历史查询功能

## 数据流向

数据从底层到顶层单向流动：
1. 数据采集层捕获原始网络流量
2. 数据处理层对原始数据进行特征工程
3. 检测算法层使用机器学习模型进行检测
4. 应用展示层将检测结果通过 Web 界面展示给用户