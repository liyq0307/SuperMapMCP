#!/usr/bin/env python3
"""
SuperMap MCP Client - Simple client to connect to the SuperMap MCP server
"""

import logging
from mcp.server.fastmcp import FastMCP
from iobjectspy import data, conversion, enums

mcp = FastMCP(
    "supermap_server",
    description="SuperMap integration through the Model Context Protocol")

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SuperMapMCPServer")

def get_datasource():
    connInfo = (data.DatasourceConnectionInfo().
                set_type(enums.EngineType.PGGIS).
                set_server('ip').
                set_database('db').
                set_alias('test').
                set_user('user').
                set_password('password'))
    datasource = data.open_datasource(connInfo)
    if datasource is None:
        raise Exception("Could not open datasource")
    else:
        logger.info("Successfully connected to SuperMap")
        
    return datasource
        
@mcp.tool(name="import_data", description="Import a shapefile to datasource")
def import_data(file_path: str) -> bool:
    datasource = get_datasource()
    if datasource is None:
        logger.error("Datasource is None")
        return False
    
    # Import the shapefile
    bImport = False

    try:
        b = conversion.import_shape(file_path, datasource)
        logger.info(f"Successfully imported {file_path} to datasource")
        bImport = (len(b) == 1)
    except Exception as e:
        logger.error(f"Failed to import {file_path}: {str(e)}")
        return False
    finally:
        datasource.close()
        logger.info("Datasource closed after import")

    return bImport
        
def main():
    """Run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
