from app.schemas.v1.shared_models import FeatureModel

# Test if we can initialize a model with nan values in the features


def test_feature_model_complete():
    fm = FeatureModel(
        name='Test_all_fields_filled',
        data=[
                3.5,
                3.1,
                2.56142
            ],
        unit="m/s",
        type="weather_data"
    )
    assert fm.name == 'Test_all_fields_filled'


def test_feature_model_nan():
    fm = FeatureModel(
        name='Test_some_nans',
        data=[
                'NaN',
                'null',
                2.56142
            ],
        unit="m/s",
        type="weather_data"
    )
    assert fm.name == 'Test_some_nans'