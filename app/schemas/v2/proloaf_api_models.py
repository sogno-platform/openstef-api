from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class EarlyStopping(BaseModel):
    patience: Optional[int] = Field(7, title='Patience')
    verbose: Optional[bool] = Field(False, title='Verbose')
    delta: Optional[float] = Field(0.0, title='Delta')


class TrainingRun(BaseModel):
    optimizer_name: Optional[str] = Field('adam', title='Optimizer Name')
    learning_rate: Optional[float] = Field(0.0001, title='Learning Rate')
    max_epochs: Optional[int] = Field(100, title='Max Epochs')
    # early_stopping: Optional[EarlyStopping] = None
    batch_size: Optional[int] = Field(None, title='Batch Size')
    history_horizon: Optional[int] = Field(24, title='History Horizon')
    forecast_horizon: Optional[int] = Field(24, title='Forecast Horizon')
    patience: Optional[int] = Field(7, title='Patience')
    delta: Optional[float] = Field(0.0, title='Minimal imporvement per Epoch')

class EncoderDecoder(BaseModel):
    rel_linear_hidden_size: Optional[float] = Field(1.0, title='Rel Linear Hidden Size')
    rel_core_hidden_size: Optional[float] = Field(1.0, title='Rel Core Hidden Size')
    core_layers: Optional[int] = Field(1, title='Core Layers')
    dropout_fc: Optional[float] = Field(0.0, title='Dropout Fc')
    dropout_core: Optional[float] = Field(0.0, title='Dropout Core')
    core_net: Optional[str] = Field('torch.nn.GRU', title='Core Net')
    relu_leak: Optional[float] = Field(0.01, title='Relu Leak')


class ModelWrapper(BaseModel):
    training: TrainingRun
    model: EncoderDecoder
    name: Optional[str] = Field('model', title='Name')
    target_id: Optional[Union[List[str], List[int]]] = Field(
        ['load'], title='Target Id'
    )
    encoder_features: List[str] = Field(..., title='Encoder Features')
    decoder_features: List[str] = Field(..., title='Decoder Features')
    metric: Optional[str] = Field('NllGauss', title='Metric')
    metric_options: Optional[Dict[str, Any]] = Field(None, title='Metric Options')
