"""
Crash Reporter Module for Strod-Service Technology Application

This module provides comprehensive error logging and crash reporting functionality
to help diagnose and fix issues in the application.
"""
import sys
import os
import logging
import traceback
from datetime import datetime
from pathlib import Path
import platform
import json
from typing import Dict, Any, Optional

# Add the src directory to the Python path to allow imports
src_path = Path(__file__).resolve().parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path.parent))

from strodservice.utils.logger import setup_logger


class CrashReporter:
    """
    A comprehensive crash reporter that captures and logs application errors
    for detailed analysis and debugging.
    """
    
    def __init__(self, app_name: str = "Strod-Service Technology"):
        self.app_name = app_name
        self.logger = setup_logger(name="crash_reporter", level=logging.ERROR)
        self.crash_dir = Path("crash_reports")
        self.crash_dir.mkdir(exist_ok=True)
        
        # Set up global exception handler
        sys.excepthook = self.global_exception_handler
        
    def global_exception_handler(self, exc_type, exc_value, exc_traceback):
        """
        Global exception handler that captures unhandled exceptions.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow Ctrl+C to work normally
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        self.report_crash(exc_type, exc_value, exc_traceback)
        
    def report_crash(self, exc_type, exc_value, exc_traceback, context: Optional[Dict[str, Any]] = None):
        """
        Generate and save a comprehensive crash report.
        
        Args:
            exc_type: Exception type
            exc_value: Exception value
            exc_traceback: Exception traceback
            context: Additional context information (optional)
        """
        try:
            # Create crash report data
            crash_data = self._generate_crash_report(exc_type, exc_value, exc_traceback, context)
            
            # Save the crash report to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            crash_file = self.crash_dir / f"crash_report_{timestamp}.json"
            
            with open(crash_file, 'w', encoding='utf-8') as f:
                json.dump(crash_data, f, indent=2, ensure_ascii=False, default=str)
                
            # Also save a text version for easier reading
            text_file = self.crash_dir / f"crash_report_{timestamp}.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(self._format_crash_report_text(crash_data))
            
            # Log the crash
            self.logger.error(f"Crash report generated: {crash_file}")
            print(f"❌ Application crashed! Report saved to: {crash_file}")
            
        except Exception as e:
            # If we can't generate a crash report, at least log the original error
            print(f"❌ Critical error occurred and crash reporter failed: {e}")
            print(f"Original error: {exc_value}")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    
    def _generate_crash_report(self, exc_type, exc_value, exc_traceback, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate comprehensive crash report data.
        """
        # Get system information
        system_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'python_implementation': platform.python_implementation(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'node': platform.node(),
        }
        
        # Get application information
        app_info = {
            'app_name': self.app_name,
            'app_version': getattr(self, '_get_app_version', lambda: 'unknown')(),
            'working_directory': str(Path.cwd()),
            'executable_path': sys.executable,
            'command_line_args': sys.argv,
        }
        
        # Format exception information
        exception_info = {
            'type': exc_type.__name__,
            'message': str(exc_value),
            'traceback': self._format_traceback(exc_traceback),
        }
        
        # Get local variables from the frame where the exception occurred
        local_vars = self._get_local_variables(exc_traceback)
        
        # Get module information
        modules_info = {name: getattr(module, '__version__', 'unknown') 
                       for name, module in sys.modules.items() 
                       if hasattr(module, '__version__')}
        
        # Build the crash report
        crash_report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': system_info,
            'app_info': app_info,
            'exception_info': exception_info,
            'local_variables': local_vars,
            'loaded_modules': modules_info,
            'context': context or {},
        }
        
        return crash_report
    
    def _format_traceback(self, exc_traceback) -> str:
        """
        Format the traceback as a string.
        """
        import traceback
        return ''.join(traceback.format_tb(exc_traceback))
    
    def _get_local_variables(self, exc_traceback) -> Dict[str, Any]:
        """
        Extract local variables from the frame where the exception occurred.
        """
        if exc_traceback is None:
            return {}
        
        # Get the frame where the exception occurred
        frame = exc_traceback.tb_frame
        local_vars = {}
        
        # Add local variables (be careful not to include sensitive data)
        for name, value in frame.f_locals.items():
            try:
                # Limit the size of the values to avoid huge reports
                str_value = str(value)
                if len(str_value) > 1000:
                    str_value = str_value[:1000] + '... (truncated)'
                local_vars[name] = str_value
            except:
                local_vars[name] = '<unable to convert to string>'
        
        return local_vars
    
    def _format_crash_report_text(self, crash_data: Dict[str, Any]) -> str:
        """
        Format the crash report as human-readable text.
        """
        lines = []
        lines.append(f"=== {self.app_name} Crash Report ===")
        lines.append(f"Timestamp: {crash_data['timestamp']}")
        lines.append("")
        
        lines.append("=== System Information ===")
        for key, value in crash_data['system_info'].items():
            lines.append(f"{key}: {value}")
        lines.append("")
        
        lines.append("=== Application Information ===")
        for key, value in crash_data['app_info'].items():
            lines.append(f"{key}: {value}")
        lines.append("")
        
        lines.append("=== Exception Information ===")
        lines.append(f"Type: {crash_data['exception_info']['type']}")
        lines.append(f"Message: {crash_data['exception_info']['message']}")
        lines.append("")
        lines.append("Traceback:")
        lines.append(crash_data['exception_info']['traceback'])
        lines.append("")
        
        if crash_data['local_variables']:
            lines.append("=== Local Variables ===")
            for name, value in crash_data['local_variables'].items():
                lines.append(f"{name}: {value}")
            lines.append("")
        
        if crash_data['context']:
            lines.append("=== Context ===")
            for key, value in crash_data['context'].items():
                lines.append(f"{key}: {value}")
            lines.append("")
        
        lines.append("=== Loaded Modules ===")
        for name, version in list(crash_data['loaded_modules'].items())[:10]:  # Limit to first 10
            lines.append(f"{name}: {version}")
        
        return '\n'.join(lines)
    
    def _get_app_version(self) -> str:
        """
        Get application version (placeholder - implement as needed).
        """
        return "1.0.0"
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any]):
        """
        Log an error with additional context information.
        
        Args:
            error: The exception that occurred
            context: Additional context information
        """
        self.logger.error(f"Error occurred: {str(error)}", extra={'context': context})
        self.report_crash(type(error), error, error.__traceback__, context)


# Global crash reporter instance
crash_reporter = CrashReporter()


def setup_crash_reporting():
    """
    Set up crash reporting for the application.
    This should be called early in the application startup.
    """
    global crash_reporter
    crash_reporter = CrashReporter()
    return crash_reporter


def get_crash_reporter():
    """
    Get the global crash reporter instance.
    """
    global crash_reporter
    return crash_reporter


def capture_exception(error: Exception, context: Optional[Dict[str, Any]] = None):
    """
    Capture an exception and generate a crash report.
    
    Args:
        error: The exception to capture
        context: Additional context information
    """
    global crash_reporter
    crash_reporter.report_crash(type(error), error, error.__traceback__, context)


def capture_context(context: Dict[str, Any]):
    """
    Add context to the next exception that occurs.
    
    Args:
        context: Context information to add
    """
    # This is a simplified version - in a real implementation you might
    # want to store this context for the next exception
    pass


if __name__ == "__main__":
    # Example usage
    crash_reporter = CrashReporter()
    
    # Test the crash reporter with a sample exception
    try:
        # Simulate an error
        x = 1 / 0
    except Exception as e:
        crash_reporter.report_crash(type(e), e, e.__traceback__, 
                                  context={'user_action': 'division_by_zero', 'input': '0'})
    
    print("Crash reporter test completed. Check the crash_reports directory.")