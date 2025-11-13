"""
Central configuration for Investment Research Dashboard
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()

@dataclass
class APIConfig:
    """API Server configuration"""
    base_url: str = "http://192.168.10.56:3000"
    timeout: int = 30  # seconds
    retry_attempts: int = 3
    retry_delay: int = 5  # seconds between retries

    # Endpoint paths
    health_endpoint: str = "/health"
    status_endpoint: str = "/api/status"
    summary_endpoint: str = "/api/summary"
    latest_endpoint: str = "/api/latest"
    maxpain_endpoint: str = "/api/maxpain"
    chat_endpoint: str = "/api/chat"
    export_endpoint: str = "/api/export"

    def get_url(self, endpoint: str) -> str:
        """Construct full URL for an endpoint"""
        return f"{self.base_url}{endpoint}"


@dataclass
class OllamaConfig:
    """Ollama server configuration for local LLM preprocessing"""
    base_url: str = "http://192.168.10.52:11434"
    api_endpoint: str = "/api/generate"
    model: str = "gpt-oss:20b"
    timeout: int = 300  # 5 minutes for large processing

    def get_url(self) -> str:
        """Construct full Ollama API URL"""
        return f"{self.base_url}{self.api_endpoint}"


@dataclass
class PathConfig:
    """File system paths"""
    # Scout is in project/scout/, so parent is project root
    project_root: Path = PROJECT_ROOT.parent

    # Data directories (root-level)
    research_dir: Path = project_root / "Research"
    toolbox_dir: Path = project_root / "Toolbox"
    scripts_dir: Path = project_root / "scripts"

    # Scout output directory
    scout_dir: Path = PROJECT_ROOT

    # Research subdirectories
    twitter_dir: Path = research_dir / "X"
    cache_dir: Path = research_dir / ".cache"

    # Scout output files
    dash_md: Path = scout_dir / "dash.md"
    dash_html: Path = scout_dir / "dash.html"

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        for dir_path in [
            self.research_dir,
            self.twitter_dir,
            self.cache_dir
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)


@dataclass
class WorkflowConfig:
    """Workflow execution settings"""
    # RECON phase settings
    recon_cleanup_days: int = 3  # Keep last N days of data
    recon_parallel_execution: bool = True

    # Data freshness thresholds (in hours)
    max_data_age_hours: int = 1  # Alert if data older than this

    # Signal calculation weights (must sum to 100)
    signal_weights: dict = None

    def __post_init__(self):
        if self.signal_weights is None:
            self.signal_weights = {
                'trend': 30,
                'breadth': 25,
                'volatility': 20,
                'sentiment': 15,
                'technical': 10
            }


@dataclass
class Config:
    """Main configuration object"""
    api: APIConfig = None
    ollama: OllamaConfig = None
    paths: PathConfig = None
    workflow: WorkflowConfig = None

    # Environment
    environment: str = os.getenv('ENVIRONMENT', 'development')
    debug_mode: bool = os.getenv('DEBUG', 'False').lower() == 'true'

    def __post_init__(self):
        if self.api is None:
            self.api = APIConfig()
        if self.ollama is None:
            self.ollama = OllamaConfig()
        if self.paths is None:
            self.paths = PathConfig()
        if self.workflow is None:
            self.workflow = WorkflowConfig()

    def validate(self) -> bool:
        """Validate configuration"""
        # Check if critical paths exist
        if not self.paths.research_dir.exists():
            print(f"Warning: Research directory not found: {self.paths.research_dir}")
            return False

        if not self.paths.scout_dir.exists():
            print(f"Warning: Scout directory not found: {self.paths.scout_dir}")
            return False

        return True

    def initialize(self):
        """Initialize configuration - create directories, validate settings"""
        self.paths.ensure_directories()
        if self.debug_mode:
            print("Configuration initialized:")
            print(f"  API: {self.api.base_url}")
            print(f"  Ollama: {self.ollama.base_url}")
            print(f"  Project root: {PROJECT_ROOT}")
            print(f"  Environment: {self.environment}")


# Global configuration instance
config = Config()

# Initialize on import
if os.getenv('AUTO_INIT_CONFIG', 'true').lower() == 'true':
    config.initialize()


# Helper functions for common operations
def get_api_url(endpoint: str) -> str:
    """Get full API URL for an endpoint"""
    return config.api.get_url(endpoint)


def get_ollama_url() -> str:
    """Get Ollama API URL"""
    return config.ollama.get_url()


def get_research_path(category: str) -> Path:
    """Get path for a research category (X only)"""
    category_map = {
        'twitter': config.paths.twitter_dir,
        'x': config.paths.twitter_dir,
        'cache': config.paths.cache_dir
    }
    return category_map.get(category.lower(), config.paths.research_dir)


if __name__ == "__main__":
    # Test configuration
    print("Configuration Test")
    print("=" * 50)
    print(f"API Base URL: {config.api.base_url}")
    print(f"Ollama URL: {config.ollama.base_url}")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Research Dir: {config.paths.research_dir}")
    print(f"Scout dash.md: {config.paths.dash_md}")
    print(f"Scout dash.html: {config.paths.dash_html}")
    print("\nValidation:", "PASSED" if config.validate() else "FAILED")
