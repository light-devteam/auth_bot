import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import FastAPI

from src.app import App


class TestApp:
    host = '0.0.0.0'
    port = 8080
    workers = 2
    app = App(host=host, port=port, workers=workers)

    def test_singleton(self, app: App) -> None:
        assert self.app is app

    def test_api_initiation(self) -> None:
        assert isinstance(self.app.api, FastAPI)

    def test_docs_configuration(self) -> None:
        assert self.app.api.docs_url == '/swagger'

    @patch('src.app.bot.run', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_lifespan(
        self,
        bot_run_mock: AsyncMock,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        lifespan = self.app.lifespan(FastAPI())
        async with lifespan:
            bot_run_mock.assert_called_once()
            assert 'App started' in caplog.text
            assert 'App finished' not in caplog.text
        assert 'App finished' in caplog.text

    @patch('src.app.uvicorn.run')
    def test_app_run(self, mock_uvicorn_run: MagicMock):
        self.app.run()
        mock_uvicorn_run.assert_called_once()
        call_args = mock_uvicorn_run.call_args[1]
        assert call_args['host'] == self.host
        assert call_args['port'] == self.port
        assert call_args['workers'] == self.workers
        assert call_args['app'] is self.app.api

    def test_api_property(self) -> None:
        assert self.app.api is self.app._App__api
